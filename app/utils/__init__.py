import traceback
from functools import wraps
from flask import request, current_app
from flask.views import MethodView


from sqlalchemy import inspect, text

from app.api.models.models import db
from app import constants as const, messages as msg

from .schemas import (API_CONFIG_BODY_VALIDATOR,
                      API_CONFIG_QUERY_PARAMS_VALIDATOR, realtion_schema,
                      schema_columns)
from .validator import none_validator, customize_route
from .exceptions import ValidationError
from .serializer import serialize_response, deserialize
from .entity import Requests

logger = const.logger


def paginate_response(page, page_size, query):

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all(), query.count()


def delete_sqllite_data():

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    for table in tables:
        if table in const.NOT_DELETE_TABLE:
            continue
        db.session.execute(text(f"DELETE FROM {table};"))
        logger.info("deleted data for %s", table)

    db.session.commit()
    db.session.execute(text("VACUUM;"))
    db.session.commit()
    logger.info("Database compacted and all rows deleted.")


def delete_main_db_data(dialect):

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    for table in tables:
        if table in const.NOT_DELETE_TABLE:
            continue
        if dialect == const.POSTGRESQL:
            db.session.execute(
                text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
            )
        else:
            db.session.execute(text(f"TRUNCATE TABLE {table};"))
    db.session.commit()
    logger.info("Database compacted and all rows deleted.")


def __class_error_handler(func):

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValidationError as e:
            return e._FORMAT_EXCEPTION
        except Exception as e:
            logger.info("error %s", e)
            logger.info("error traceback %s", traceback.format_exc())
            return {"error": msg.GENERAL_ERROR}, 500

    return wrapper


def class_error_handler(cls):
    decorate_methods = const.DECORATE_METHODS
    for attr_name, attr_value in cls.__dict__.items():
        if (
            callable(attr_value)
            and not attr_name.startswith("__")
            and attr_name in decorate_methods
        ):
            decorated_func = __class_error_handler(attr_value)
            setattr(cls, attr_name, decorated_func)
    return cls


def __class_api_request(func):

    def wrapper(self, *args, **kwargs):
        path = str(request.url_rule)
        method = request.method
        app = current_app
        api_config = app.config.get("API_CONFIG", {})

        dedicated_config = api_config.get(path, {})
        data_config = dedicated_config.get(f"{method.upper()}_data", {})
        _query_params = data_config.get('query_params', {})
        _payload = data_config.get('body', {})

        query_params = clean_queryparams(_query_params, request.args)
        data = {}
        if request.data:
            data = request.get_json()
        payload = clean_payload(_payload, data)

        _request = Requests(
            method=method,
            path=path,
            query_params=query_params,
            body=payload
        )

        MethodView._request = _request
        resp = func(self, **kwargs)

        return resp

    return wrapper


def class_api_request(cls):
    decorate_methods = const.DECORATE_METHODS
    for attr_name, attr_value in cls.__dict__.items():
        if (
            callable(attr_value)
            and not attr_name.startswith("__")
            and attr_name in decorate_methods
        ):
            decorated_func = __class_api_request(attr_value)
            setattr(cls, attr_name, decorated_func)
    return cls


def clean_queryparams(query_params, request_query_param):

    request_query_param = recursive_dict_to_lower(request_query_param) 
    query_param = deserialize(query_params, dict(request_query_param))
    return query_param


def clean_payload(payload, request_payload):
    request_payload = recursive_dict_to_lower(request_payload)
    payload = deserialize(payload, request_payload)
    return payload


def recursive_dict_to_lower(_dict):
    new_dict = {}
    for key, value in _dict.items():
        # Convert the key to lowercase
        new_key = key.lower()
        if isinstance(value, dict):
            # If the value is a dictionary, call the function recursively
            new_dict[new_key] = recursive_dict_to_lower(value)
        elif isinstance(value, list):
            # If the value is a list, handle each item
            new_dict[new_key] = [recursive_dict_to_lower(item) if isinstance(item, dict) else item for item in value]
        else:
            # If it's a value (not a dict or list), just copy the value
            new_dict[new_key] = value
    return new_dict


def _custom_api_validation(payload, entity):
    model_fields = entity._asdict()
    for field, value in payload.items():
        arg_name = value.get("arg_name")
        if not arg_name and field not in model_fields.get("body"):
            raise ValidationError(msg=msg.API_CONF_FIELD_ARG_NOT_MATCH)
        if arg_name and arg_name.lower() not in model_fields.get("body"):
            raise ValidationError(msg=msg.API_CONF_FIELD_ARG_NOT_MATCH)


def mod_col(column):
    if not column:
        return column

    split_col = column.split(" ")
    if len(split_col) > 1:
        column = "_".join(split_col)
    return column


def mod_request(request, model_entity):

    id = request.body.pop("id", None)
    pk = request.body.pop("pk", None)

    if hasattr(model_entity, "pk") and id:
        request.body["pk"] = id
    elif hasattr(model_entity, "id") and pk:
        request.body["id"] = pk
