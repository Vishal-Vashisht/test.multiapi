from flask import Blueprint, request
from flask.views import MethodView
from app.api.services import cloudnary
from app.utils import class_error_handler, class_api_request


@class_error_handler
@class_api_request
class UploadToCloudnary(MethodView):

    def post(self):

        body, status = {}, 200
        if request.files:
            body, status = cloudnary.cloudnary_upload()

        return body, status


cloudnary_bp = Blueprint("cloudnary", __name__, url_prefix="/api/v1/cloudnary")
cloudnary_bp.add_url_rule(
    "/upload/", view_func=UploadToCloudnary.as_view("cloudnary_upload")
)  # noqa
