from flask import Blueprint
from flask.views import MethodView


class SampleList(MethodView):

    def get(self):

        return ({"response": "success",
                 "message": "Tell me a funny joke"},
                200)


sample_bp = Blueprint("sample", __name__, url_prefix="/api/v1/sample")
sample_bp.add_url_rule("/", view_func=SampleList.as_view("sampelList-get")) # noqa
