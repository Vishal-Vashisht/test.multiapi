from flask import Blueprint, current_app, request
from flask.views import MethodView

from app.api.models.models import APIConfig, Entity
from app.api.services import dynamic_api as dapi_service
from app.constants import logger
from app.utils import ValidationError, class_error_handler, class_api_request


@class_error_handler
@class_api_request
class DynamicAPIView(MethodView):

    def get(self, pk=None):
        model, api_config_entity = dapi_service.get_model(
            current_app, self._request)
        resp = dapi_service.get_data(model, api_config_entity, pk)
        return resp, 200

    def post(self):
        model, api_config_entity = dapi_service.get_model(
            current_app, self._request)
        resp = dapi_service.post_data(model, api_config_entity)
        return resp, 201

    def put(self, pk=None):
        model, api_config_entity = dapi_service.get_model(
            current_app, self._request)
        resp = dapi_service.post_data(model, api_config_entity)
        return resp, 200

    def patch(self, pk=None):
        model, api_config_entity = dapi_service.get_model(
            current_app, self._request)
        resp = dapi_service.post_data(model, api_config_entity)
        return resp, 200

    def delete(self, pk):
        model, api_config_entity = dapi_service.get_model(
            current_app, self._request)
        resp = dapi_service.post_data(model, api_config_entity)
        return resp, 204


dynamic_bp = Blueprint("dynamic_apis", __name__, url_prefix="/api/v1/")
dynamic_bp.view_class = DynamicAPIView
