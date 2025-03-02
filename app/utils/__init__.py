import traceback
from functools import wraps

from sqlalchemy import inspect, text

from app.api.models.models import db
from app.constants import logger

from .schemas import (API_CONFIG_BODY_VALIDATOR,
                      API_CONFIG_QUERY_PARAMS_VALIDATOR, realtion_schema,
                      schema_columns)
from .validator import none_validator
from .exceptions import ValidationError

MAIN_DB = set(("postgresql", "mysql", "oracle"))
NOT_DELETE_TABLE = set(
    (
        "alembic_version",
        "daily_data_delete",
        "internal_users",
        "task_status",
        "bg_task_response",
        "bg_tasks",
    )
)


def paginate_response(page, page_size, query):

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all(), query.count()


def delete_sqllite_data():

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    for table in tables:
        if table in NOT_DELETE_TABLE:
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
        if table in NOT_DELETE_TABLE:
            continue
        if dialect == "postgresql":
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
            return e._msg, e._code
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return {"error": "Something went wrong we are try to fix this."}, 500

    return wrapper


def class_error_handler(cls):
    decorate_methods = set(("get", "post", "delete", "patch", "put", "head"))
    for attr_name, attr_value in cls.__dict__.items():
        if (
            callable(attr_value)
            and not attr_name.startswith("__")
            and attr_name in decorate_methods
        ):
            decorated_func = __class_error_handler(attr_value)
            setattr(cls, attr_name, decorated_func)
    return cls
