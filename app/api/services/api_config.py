from jsonschema import Draft7Validator

from app.api.models.models import APIConfig, Entity
from app.utils import (
    API_CONFIG_BODY_VALIDATOR,
    API_CONFIG_QUERY_PARAMS_VALIDATOR,
    ValidationError,
    none_validator,
    customize_route,
    _custom_api_validation
)

from app.constants import API_PREFIX


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
        print("dfd1")
        errors.append({"name": e.path[0], "error": e.message})

    query_validator = Draft7Validator(API_CONFIG_QUERY_PARAMS_VALIDATOR)
    for e in query_validator.iter_errors(entity.query_params):
        print("dfd")
        errors.append({"name": e.path[0], "error": e.message})

    if errors:
        raise ValidationError(errors)


def create_api_config(entity):

    if not Entity.query.get(entity.entity):
        raise ValidationError({"error": "Entity not exists"})

    if APIConfig.query.filter_by(name=entity.name).first():
        raise ValidationError({"error": "Name already exists"})

    if APIConfig.query.filter_by(route=entity.route.lower()).first():
        raise ValidationError({"error": "Route already exists"})
    append_description = "Entitys attributes will be used as default payload"
    route = customize_route(api_route=entity.route)

    print(entity)
    api_inst = APIConfig(
        name=entity.name,
        route=f"{API_PREFIX}{route}",
        method=entity.method,
        description=f"{append_description} {entity.description}",
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
