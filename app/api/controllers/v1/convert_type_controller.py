from flask import Blueprint, request, Response
from flask.views import MethodView
from app.constants import logger
from app.utils.helpers import _handle_export


class ConvertToType(MethodView):

    def post(self):

        data = request.get_json()
        logger.info("data received from api %s", data)
        logger.info("type of data : - %s", type(data))

        if not data:
            data = {}

        if "error" in data:
            error = data.get("error", {})
            error_msg = error.pop("error_msg", "An error occurred")
            error_code = error.pop("error_code", "500")
            extra_fields = {k: v for k, v in error.items()}
            request_resonse = {
                "error_msg": error_msg,
                "error_code": error_code,
                **extra_fields
            }
            return Response(
                response=request_resonse,
                status=int(error_code),
                mimetype="application/json",
            )

        if isinstance(data, dict):
            export = data.pop("export", None)
            allow_filters = data.pop("allow_filters", "true")
            if export in ["xlsx", "xls"]:
                return _handle_export(
                    export,
                    body=data,
                    allow_filters=allow_filters,
                )

        return data


convert_bp = Blueprint("covert_type", __name__, url_prefix="/api/v1/echo")
convert_bp.add_url_rule("/", view_func=ConvertToType.as_view("post_covert_data")) # noqa