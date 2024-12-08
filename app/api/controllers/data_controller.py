import json

from flask import Blueprint, request
from flask.views import MethodView

from app.api.entity import (ParallelEntity, UserAppEntity, UserAppPostEntity,
                            UserCartEntity)
from app.api.models.models import (ParallelData, UserApp, UserAppPostData,
                                   UserCart, db)
from app.constants import logger
from app.utils import paginate_response


class DataAPIView(MethodView):

    def get(self):
        page = request.args.get('page', default=1, type=int)
        size = request.args.get('size', default=10, type=int)

        user_app_data = paginate_response(
            page=page,
            page_size=size,
            query=UserApp.query
        )

        user_cart_data = paginate_response(
            page=page,
            page_size=size,
            query=UserCart.query
        )

        parallel_data = paginate_response(
            page=page,
            page_size=size,
            query=ParallelData.query
        )

        user_app_post_data = paginate_response(
            page=page,
            page_size=size,
            query=UserAppPostData.query
        )

        response = {
            "user_app_data": [UserAppEntity(
                pk=user_app.user_id,
                name=user_app.name,
                email=user_app.email,
                gender=user_app.gender,
                refrence_id=user_app.refrence_id
            )._asdict() for user_app in user_app_data],
            "user_cart_data": [UserCartEntity(
                pk=user_cart.user_id,
                name=user_cart.name,
                email=user_cart.email,
                gender=user_cart.gender,
                refrence_id=user_cart.refrence_id
            )._asdict() for user_cart in user_cart_data],
            "parallel_data": [ParallelEntity(
                pk=para_data.user_id,
                name=para_data.name,
                email=para_data.email,
                gender=para_data.gender,
                refrence_id=para_data.refrence_id
            )._asdict() for para_data in parallel_data],
            "user_app_post_data": [UserAppPostEntity(
                pk=app_post_data.user_id,
                name=app_post_data.name,
                email=app_post_data.email,
                gender=app_post_data.gender,
                refrence_id=app_post_data.refrence_id
            )._asdict() for app_post_data in user_app_post_data],
            "page": page,
            "page_size": size
        }
        return response, 200


data_bp = Blueprint("data_bp", __name__, url_prefix="/api/v1/data")
data_bp.add_url_rule("/", view_func=DataAPIView.as_view("Data-list-create"))