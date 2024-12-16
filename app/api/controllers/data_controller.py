import json

from flask import Blueprint, request
from flask.views import MethodView
from app.api.services.data_fetch import fetch_data


class DataAPIView(MethodView):

    def get(self):
        page = request.args.get("page", default=1, type=int)
        size = request.args.get("size", default=10, type=int)

        response = fetch_data(page, size)
        return response, 200

    def post(self):
        data = request.get_json()

        page = data.get("page", 1)
        size = data.get("size", 10)

        response = fetch_data(page, size)
        return response, 200


data_bp = Blueprint("data_bp", __name__, url_prefix="/api/v1/data")
data_bp.add_url_rule("/", view_func=DataAPIView.as_view("Data-list-create"))
