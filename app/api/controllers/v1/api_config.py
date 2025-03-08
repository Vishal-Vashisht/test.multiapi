from flask import Blueprint, request
from flask.views import MethodView
from app.constants import logger
from app.api.entity import APIConfigEntity
from app.api.services import api_config as apiservice
from app.utils import class_error_handler, class_api_request


@class_error_handler
@class_api_request
class APIConfigView(MethodView):

    def get(self, pk=None):
        resp = apiservice.get_api_config(self._request, pk)
        return resp, 200

    def post(self):
        payload = request.get_json()
        entity = APIConfigEntity(**payload)
        apiservice.validations(entity)
        response = apiservice.create_api_config(entity=entity)
        return response


apiconfig_bp = Blueprint("api_config", __name__, url_prefix="/api/v1/api-config") # noqa
apiconfig_bp.add_url_rule("/", view_func=APIConfigView.as_view("api_conf"))  # noqa
apiconfig_bp.add_url_rule("/<int:pk>/", view_func=APIConfigView.as_view("api_conf_id"))  # noqa