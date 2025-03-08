import ast
from typing import Tuple

from flask import app

from app.api.entity import DynamicApiConfEntity
from app.api.models.models import APIConfig, db, dynamic_delete, dynamic_save
from app.utils import (Requests, ValidationError, mod_request,
                       serialize_response)
from app import messages


def get_model(current_app: app, request: Requests) -> Tuple:
    path = request.path
    api_config = APIConfig.query.filter_by(route=path[1:]).first()
    api_conf_entity = preapare_dyamic_api_conf(api_config)
    if not api_config:
        raise ValidationError(msg=messages.DYNAMIC_API_CONF_NOT_EXIST)

    entity_name = api_conf_entity.entity_name
    model = current_app.dynamic_models.get(entity_name)
    model_entity = current_app.ENTITY.get(entity_name.lower())
    if not model:
        raise ValidationError(msg=messages.DYNAMIC_MODEL_DEF_NOT_EXIST)

    return model, api_conf_entity, model_entity


def get_data(model, api_config_entity, pk, request, model_entity):
    query_params = request.query_params
    page = query_params.pop("page", 1)
    page_size = query_params.pop("page_size", 10)

    query_set = model.query.all()
    if pk:
        query_set = model.query.get(pk)
    elif query_params:
        query_set = model.query.filter_by(**query_params).all()

    resp_fields = api_config_entity.response
    resp = serialize_response(query_set, resp_fields, model)
    return resp


def post_data(model, api_config_entity, request, named_entity):

    _entity = named_entity(**request.body)
    _save_instance = _entity._asdict()
    _save_instance.pop("pk", "")
    _save_instance.pop("id", "")

    model_save_inst = model(**_save_instance)

    dynamic_save(model_save_inst)

    resp = serialize_response(
        model_save_inst, api_config_entity.response, model
    )
    return resp


def update_data(model, api_config_entity, request, model_entity, pk):

    mod_request(request, model_entity)

    _entity = model_entity(**request.body)
    _dict_entity = _entity._asdict()
    model_pk = _entity.id

    if not pk:
        pk = model_pk
    if not pk and pk == 0:
        raise ValidationError(messages.DYNAMIC_PK_REQUIRED)

    _entity = _entity._replace(id=pk)
    if pk:
        model_ins = model.query.get(pk)
    elif model_pk:
        model_ins = model.query.get(pk)

    for col_name in model.__table__.columns.keys():
        def_val = getattr(model_ins, col_name)
        val = ""
        if hasattr(_entity, col_name):
            val = getattr(_entity, col_name)

        if col_name in _dict_entity:
            setattr(
                model_ins, col_name,
                val or def_val
            )

    dynamic_save(model_ins)
    resp = serialize_response(
        model_ins, api_config_entity.response, model
    )
    return resp


def delete_data(model, api_config_entity, request, model_entity, pk):

    mod_request(request, model_entity)

    print(request)
    _entity = model_entity(**request.body)
    _dict_entity = _entity._asdict()
    model_pk = _entity.id

    if not pk:
        pk = model_pk
    if not pk and pk == 0:
        raise ValidationError(msg=messages.DYNAMIC_PK_REQUIRED)

    if pk:
        model_ins = model.query.get(pk)
    elif model_pk:
        model_ins = model.query.get(pk)

    dynamic_delete(model_ins)

    resp = serialize_response(
        model_ins, api_config_entity.response, model
    )
    return resp


def preapare_dyamic_api_conf(api_conf: APIConfig) -> DynamicApiConfEntity:

    response_field = api_conf.response
    body = api_conf.response
    query_params = api_conf.query_params

    obj = dict(
        response=response_field,
        query_params=query_params,
        body=body,
        entity_name=api_conf.entity_rel.entity_name,
    )
    if isinstance(response_field, str) and response_field.startswith("["):
        obj["response"] = ast.literal_eval(response_field)

    if isinstance(body, str) and body.startswith("{"):
        obj["body"] = ast.literal_eval(body)

    if isinstance(query_params, str) and query_params.startswith("{"):
        obj["query_params"] = ast.literal_eval(query_params)

    return DynamicApiConfEntity(**obj)
