from flask import request
import ast

from app.api.models.models import APIConfig, Entity, db
from app.utils import ValidationError, serialize_response
from app.api.entity import APIConfigEntity


def get_model(current_app, request):
    path = request.path
    api_config = APIConfig.query.filter_by(route=path[1:]).first()
    if not api_config:
        raise ValidationError({"error": "Api config not exists"})

    entity_name = api_config.entity_rel.entity_name
    model = current_app.dynamic_models.get(entity_name)
    named_entity = current_app.ENTITY.get(entity_name.lower())
    if not model:
        raise ValidationError({"error": "Model defination not found"})

    return model, api_config, named_entity


def get_data(model, api_config_entity, pk, request, named_entity):
    query_params = request.query_params
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


def post_data(model, api_config_entity, request, named_entity):

    # _api_config = APIConfigEntity()
    # _entity = named_entity(**request.body)
    # _save_instance = _entity._asdict()
    # _save_instance.pop("pk", "")
    # _save_instance.pop("id", "")

    # print(_save_instance)
    # print("ddfd", model.__tablename__)
    model_ins = model.query.count()
    print(model_ins)
    model_save_inst = model(name="vishal", email="vs")
    model_save_inst.save()
    # db.session.refresh(model_save_inst)

    # db.session.add(model_save_inst)
    # db.session.commit()
    # print(hasattr(model_save_inst, 'save'))
    # print(model_save_inst._sa_instance_state._commit())
    return _save_instance
