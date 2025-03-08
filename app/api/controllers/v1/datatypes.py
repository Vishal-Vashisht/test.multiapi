from flask import Blueprint
from flask.views import MethodView
from app.constants import logger
from app.utils import class_error_handler, class_api_request
from app.api.services import datatype as dtypeservice


@class_error_handler
@class_api_request
class EntityView(MethodView):

    def get(self, pk=None):
        resp = dtypeservice.get_data(self._request, pk)
        return resp, 200


datatype_bp = Blueprint("datatypes", __name__, url_prefix="/api/v1/datatypes")
datatype_bp.add_url_rule("/", view_func=EntityView.as_view("entity"))  # noqa
