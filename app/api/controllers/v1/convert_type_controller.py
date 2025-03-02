from flask import Blueprint, request
from flask.views import MethodView
from app.constants import logger


class ConvertToType(MethodView):

    def post(self):

        data = request.get_json()
        logger.info("data received from api %s", data)
        logger.info("type of data : - %s", type(data))

        return data


convert_bp = Blueprint("covert_type", __name__, url_prefix="/api/v1/echo")
convert_bp.add_url_rule("/", view_func=ConvertToType.as_view("post_covert_data")) # noqa