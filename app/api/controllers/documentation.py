from flask import Blueprint, current_app
from flask.views import MethodView
from app.custom_cache import Cache
from ..services import documentation


class DocClass(MethodView):

    def get(self):

        doc = documentation.prepare_api_documentation(app=current_app)
        return (doc, 200)


docapi_view = Blueprint(
    "docview_bp",
    __name__,
    url_prefix="/",
)

docapi_view.add_url_rule("doc/", view_func=DocClass.as_view("docapi_view"))
