from flask import request
import ast

from app.api.models.models import APIConfig, Entity
from app.utils import ValidationError, serialize_response


def get_model(current_app, request):
    path = request.path
    api_config = APIConfig.query.filter_by(route=path[1:]).first()
    if not api_config:
        raise ValidationError({"error": "Api config not exists"})

    entity_name = api_config.entity_rel.entity_name
    model = current_app.dynamic_models.get(entity_name)
    if not model:
        raise ValidationError({"error": "Model defination not found"})

    return model, api_config


def get_data(model, api_config_entity, pk):
    query_params = dict(request.args)
    page = query_params.pop("page", 1)
    page_size = query_params.pop("page_size", 10)

    query_set = model.query.all()
    if pk:
        query_set = model.query.get(pk)
    elif query_params:
        query_set = model.query.filter_by(**query_params).all()

    resp_fields = api_config_entity.response
    resp = serialize_response(query_set, ast.literal_eval(resp_fields), model)
    return resp
