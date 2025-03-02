from flask import Blueprint, request, current_app
from flask.views import MethodView
from app.constants import logger


class DynamicAPIView(MethodView):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


dynamic_bp = Blueprint("dynamic_apis", __name__, url_prefix="/api/v1/")
dynamic_bp.view_class = DynamicAPIView
