from jsonschema import Draft7Validator

from app.api.models.models import APIConfig, Entity
from app.utils import (
    API_CONFIG_BODY_VALIDATOR,
    API_CONFIG_QUERY_PARAMS_VALIDATOR,
    ValidationError,
    none_validator,
    customize_route,
    _custom_api_validation,
    serialize_response
)

from app import constants, messages


def validations(entity):
    none_validator(
        entity=entity, fields_exclude={"id", "body", "query_params", "description", "created_date"}
    )
    schema_validation(entity)
    _custom_api_validation(entity.body, entity)


def schema_validation(entity):

    # body validator
    errors = []
    body_validator = Draft7Validator(API_CONFIG_BODY_VALIDATOR)
    for e in body_validator.iter_errors(entity.body):
        errors.append({"name": e.path[0], "error": e.message})

    query_validator = Draft7Validator(API_CONFIG_QUERY_PARAMS_VALIDATOR)
    for e in query_validator.iter_errors(entity.query_params):
        errors.append({"name": e.path[0], "error": e.message})

    if errors:
        raise ValidationError(errors)


def create_api_config(entity):

    if not Entity.query.get(entity.entity):
        raise ValidationError(msg=messages.API_CONF_ENTITY_NOT_EXISTS)

    if APIConfig.query.filter_by(name=entity.name).first():
        raise ValidationError(msg=messages.API_CONF_NAME_EXISTS)

    if APIConfig.query.filter_by(route=entity.route.lower()).first():
        raise ValidationError(msg=messages.API_CONF_ROUTE_EXISTS)

    route = customize_route(api_route=entity.route)

    api_inst = APIConfig(
        name=entity.name,
        route=f"{constants.API_PREFIX}{route}",
        method=entity.method,
        description=f"{messages.API_CONF_DEFAULT_DESCRIPTION}\n{entity.description}",
        body=str(entity.body),
        is_authenticated=entity.is_authenticated,
        query_params=str(entity.query_params),
        response=str(entity.response),
        entity=entity.entity,
    )

    api_inst.save()

    return {
        "pk": api_inst.id,
        "name": api_inst.name,
        "route": api_inst.route,
        "method": api_inst.method,
    }


def get_api_config(request, pk):

    query_params = request.query_params
    query_set = APIConfig.query.all()
    page = query_params.pop("page", 1)
    page_size = query_params.pop("page_size", 10)
    if pk:
        query_set = APIConfig.query.get(pk)
    if query_params:
        query_set = APIConfig.query.filter_by(**query_params).all()

    resp = serialize_response(query_set, ["*"], APIConfig)
    return resp
