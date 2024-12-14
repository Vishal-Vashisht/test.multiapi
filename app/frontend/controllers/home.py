from flask import Blueprint, render_template
from flask.views import MethodView


class HomeView(MethodView):

    def get(self):
        return render_template("home.html")


class DataView(MethodView):

    title = "Serving Data"

    def get(self):
        return render_template("data.html", title=self.title)


class LoginView(MethodView):
    title = "Serving Login"

    def get(self):
        return render_template("login.html", title=self.title)


homebp = Blueprint(
    "home_bp", __name__,
    url_prefix="/home",
    template_folder="../templates/",
    static_folder="static")
homebp.add_url_rule("/", view_func=HomeView.as_view("home_view"))
homebp.add_url_rule("/data/", view_func=DataView.as_view("data_view"))
homebp.add_url_rule("/login/", view_func=LoginView.as_view("login_view"))
