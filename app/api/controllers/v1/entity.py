from flask import Blueprint, request, current_app
from flask.views import MethodView
from app.constants import logger
from app.api.entity import CustomEntity
from app.api.services import entity as entityserivice
from app.utils import class_error_handler, class_api_request, mod_col
from app.api.models.models import db


@class_error_handler
@class_api_request
class EntityView(MethodView):

    def post(self):
        data = self._request.body
        entity = CustomEntity(**data)
        app = current_app._get_current_object()
        entityserivice.perform_validation(entity)
        entityserivice.schema_validation(entity, app)
        data = entityserivice.create_entity(entity, app)

        return data, 201

    def get(self, pk=None):
        resp = entityserivice.get_data(self._request, pk)
        return resp, 200


entity_bp = Blueprint("entity", __name__, url_prefix="/api/v1/entity")
entity_bp.add_url_rule("/", view_func=EntityView.as_view("entity"))  # noqa
entity_bp.add_url_rule(
    "/<int:pk>/", view_func=EntityView.as_view("entity_pk_get")
)  # noqa
