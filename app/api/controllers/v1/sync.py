from flask import Blueprint, current_app, request
from flask.views import MethodView

from app.api.models.models import db
from app.utils import class_error_handler
from app.api.services import sync as syncservice


@class_error_handler
class DeployView(MethodView):

    def post(self):
        app = current_app._get_current_object()
        data = request.get_json()
        res = syncservice.restart_app(app)
        return res


sync_bp = Blueprint("sync", __name__, url_prefix="/api/v1/sync")
sync_bp.add_url_rule("/", view_func=DeployView.as_view("sync"))  # noqa
