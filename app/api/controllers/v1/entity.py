from flask import Blueprint, request, current_app
from flask.views import MethodView
from app.constants import logger
from app.api.entity import CustomEntity
from app.api.services import entity as entityserivice
from app.utils import class_error_handler
from app.api.models.models import db


@class_error_handler
class EntityView(MethodView):

    def post(self):
        data = request.get_json()
        entity = CustomEntity(**data)

        entityserivice.perform_validation(entity)
        entityserivice.schema_validation(entity)
        data = entityserivice.create_entity(entity)

        return data

    def get(self):
        model = current_app.dynamic_models.get("custom_users")
        print(model.query.all())
        return {"df": "dfd"}

    def delete(self):
        pass

    def patch(self):
        pass

    def put(self):
        pass


entity_bp = Blueprint("entity", __name__, url_prefix="/api/v1/entity")
entity_bp.add_url_rule("/", view_func=EntityView.as_view("entity"))  # noqa
