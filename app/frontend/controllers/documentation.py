from flask import Blueprint, render_template
from flask.views import MethodView


class DocView(MethodView):
    title = "Serving Documentation"

    def get(self):
        return render_template("documentation.html")


docbp = Blueprint(
    "doc_bp", __name__,
    url_prefix="/",
    template_folder="../templates/",
    static_folder="static")

docbp.add_url_rule("documentation/", view_func=DocView.as_view("doc_view"))
