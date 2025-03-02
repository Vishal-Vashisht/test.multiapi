# from app.api.models.models import TestCaseQuery
from flask import Flask
from flask_cors import CORS

from app.api.controllers.v1.convert_type_controller import convert_bp
from app.api.controllers.v1.traveler_controller import travler_bp
from app.api.controllers.v1.user_controller import auth_bp
from app.api.controllers.v1.sample_controller import sample_bp
from app.api.controllers.v1.data_controller import data_bp
from app.api.controllers.v1.user_auth import user_bp
from app.api.controllers.v1.sync_async_delete_data_controller import delete_data_bp
from app.api.controllers.v1.entity import entity_bp
from app.api.controllers.v1.api_config import apiconfig_bp
from app.api.controllers.v1.documentation import docapi_view
from app.api.controllers.v1.dynamic_api import dynamic_bp
from app.api.models.models import db, migrate, insert_initial_data
from app.api.controllers.v1.sync import sync_bp
from app.scheduler import register_scheduler
from config.redis_config import redis_client
from app.middelware import register_middelware
from app.commands import register_cli_commands
from app.frontend.controllers import homebp, loginbp, docbp
from app.custom_cache import intialized_cache
from app.initial_tasks import task


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.config")
    # redis_client.init_app(app))
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    intialized_cache(app=app)
    # register_scheduler(app)
    register_middelware(app)
    register_cli_commands(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(convert_bp)
    app.register_blueprint(travler_bp)
    app.register_blueprint(sample_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(delete_data_bp)
    app.register_blueprint(docapi_view)
    app.register_blueprint(entity_bp)
    app.register_blueprint(apiconfig_bp)
    app.register_blueprint(sync_bp)

    # register forntend bps
    app.register_blueprint(homebp)
    app.register_blueprint(loginbp)
    app.register_blueprint(docbp)

    # tasks
    app.view_class = dynamic_bp.view_class
    app.block_requests = False
    app.restart_time = None
    app.restarts_in = None
    task(app=app, dynamic_bp=dynamic_bp)
    return app
