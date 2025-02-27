# from app.api.models.models import TestCaseQuery
from flask import Flask
from flask_cors import CORS

from app.api.controllers.convert_type_controller import convert_bp
from app.api.controllers.traveler_controller import travler_bp
from app.api.controllers.user_controller import auth_bp
from app.api.controllers.sample_controller import sample_bp
from app.api.controllers.data_controller import data_bp
from app.api.controllers.user_auth import user_bp
from app.api.controllers.sync_async_delete_data_controller import delete_data_bp
from app.api.controllers.documentation import docapi_view
from app.api.models.models import db, migrate, insert_initial_data
from app.scheduler import register_scheduler
from config.redis_config import redis_client
from app.middelware import register_middelware
from app.commands import register_cli_commands
from app.frontend.controllers import homebp, loginbp, docbp
from app.custom_cache import intialized_cache


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

    # register forntend bps
    app.register_blueprint(homebp)
    app.register_blueprint(loginbp)
    app.register_blueprint(docbp)
    return app
