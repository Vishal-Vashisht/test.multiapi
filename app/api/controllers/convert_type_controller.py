from flask import Blueprint, request
from flask.views import MethodView


class ConvertToType(MethodView):

    def post(self):

        data = request.get_json()
        print("data received from api", data)
        print("type of data : -", type(data))

        return data


convert_bp = Blueprint("covert_type", __name__, url_prefix="/api/v1/convert")
convert_bp.add_url_rule("/", view_func=ConvertToType.as_view("post_covert_data")) # noqa