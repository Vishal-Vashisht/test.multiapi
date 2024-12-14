from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from werkzeug.security import check_password_hash
from app.api.models.models import Users
from config.config import API_KEY


class UserLoginView(MethodView):

    def post(self):

        body, status = {"err_msg": []}, 200
        data = request.get_json()
        _username = data.get("username")
        _pass = data.get("password")

        err_msg = body.get("err_msg")

        if not _username:
            err_msg.append("username is required field")
            return body, 400

        if not _pass:
            err_msg.append("password is required field")
            return body, 400

        user_in_db = Users.query.filter(
            Users.username == _username
        ).first()

        if not user_in_db:
            err_msg.append("User does not exists.")
            return body, 400

        valid_pass = check_password_hash(user_in_db.password, _pass)
        if not valid_pass:
            err_msg.append("Provide valid password")
            return body, 400

        body["access_token"] = API_KEY
        body["msg"] = "success"
        # Create the response object
        resp = make_response(jsonify(body), status)

        # Set the access_token in the cookie
        resp.set_cookie('access_token', f"Bearer {API_KEY}")
        return resp


user_bp = Blueprint("user_bp", __name__, url_prefix="/api/v1/auth/user/login/")
user_bp.add_url_rule("/", view_func=UserLoginView.as_view("user-login")) # noqa