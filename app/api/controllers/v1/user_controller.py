from flask import Blueprint, request
from flask.views import MethodView
from app.api.models.models import UserApp, UserCart, UserAppPostData, ParallelData
from app.api.entity import UserCartEntity, UserAppEntity, ParallelEntity
from app.constants import logger


class RegisterCartUser(MethodView):

    def post(self):

        data = request.get_json()

        logger.info("data received usercart %s", data)
        if isinstance(data, list):
            data = data[0]

        usercart = UserCartEntity(**data)
        usercart = UserCart(
            name=usercart.name,
            email=usercart.email,
            gender=usercart.gender,
            refrence_id=usercart.refrence_id
        )
        usercart.save()

        return UserCartEntity(
            pk=usercart.user_id,
            name=usercart.name,
            email=usercart.email,
            gender=usercart.gender,
            refrence_id=usercart.refrence_id

        )._asdict(), 201


class RegisterAppUser(MethodView):

    def post(self):

        data = request.get_json()

        logger.info("data received %s", data)
        if isinstance(data, list):
            data = data[0]
        userapp = UserAppEntity(**data)
        userapp = UserApp(
            name=userapp.name + "--app",
            email=userapp.email,
            gender=userapp.gender,
            refrence_id=userapp.refrence_id

        )
        userapp.save()

        return UserAppEntity(
            pk=userapp.user_id,
            name=userapp.name,
            email=userapp.email,
            gender=userapp.gender,
            refrence_id=userapp.refrence_id

        )._asdict(), 201


class UserAppPostAPI(MethodView):

    def post(self):

        data = request.get_json()

        ("data received", data)
        if isinstance(data, list):
            data = data[0]
        userapppost = UserAppEntity(**data)
        userapppost = UserAppPostData(
            name=userapppost.name,
            email=userapppost.email,
            gender=userapppost.gender,
            refrence_id=userapppost.refrence_id

        )
        userapppost.save()

        return UserAppEntity(
            pk=userapppost.user_id,
            name=userapppost.name,
            email=userapppost.email,
            gender=userapppost.gender
        )._asdict(), 201


class ParallelAPI(MethodView):

    def post(self):

        data = request.get_json()
        destinantion_num = request.headers.get('Destination-Num', "--")

        logger.info("data received on parallel %s", data)
        if isinstance(data, list):
            data = data[0]
        parallel_post = ParallelEntity(**data)
        parallel_post = ParallelData(
            name=parallel_post.name + "--Para--" + str(destinantion_num),
            email=parallel_post.email,
            gender=parallel_post.gender,
            refrence_id=parallel_post.refrence_id

        )
        parallel_post.save()

        return ParallelEntity(
            pk=parallel_post.user_id,
            name=parallel_post.name,
            email=parallel_post.email,
            gender=parallel_post.gender
        )._asdict(), 201


auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
auth_bp.add_url_rule("/register/usercart/", view_func=RegisterCartUser.as_view("Registerapi")) # noqa
auth_bp.add_url_rule("/register/userapp/", view_func=RegisterAppUser.as_view("Registerapiapp")) # noqa
auth_bp.add_url_rule("/insert/user-app-post/", view_func=UserAppPostAPI.as_view("Userappdataafterpost")) # noqa
auth_bp.add_url_rule("/parallel/", view_func=ParallelAPI.as_view("parallel-destination")) # noqa

# http://127.0.0.1:5002/api/v1/auth/register/usercart/
# http://127.0.0.1:5002/api/v1/auth/register/userapp/
# http://127.0.0.1:5002/api/v1/auth/insert/user-app-post/
# http://127.0.0.1:5002/api/v1/auth/parallel/