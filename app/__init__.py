# from app.api.models.models import TestCaseQuery
from flask import Flask
from flask_cors import CORS

from app.api.controllers.convert_type_controller import convert_bp
from app.api.controllers.traveler_controller import travler_bp
from app.api.controllers.user_controller import auth_bp
from app.api.controllers.sample_controller import sample_bp
from app.api.models.models import db, migrate
from app.scheduler import register_scheduler
from config.redis_config import redis_client
from app.middelware import register_middelware


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.config")
    # redis_client.init_app(app))
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # register_scheduler(app)
    register_middelware(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(convert_bp)
    app.register_blueprint(travler_bp)
    app.register_blueprint(sample_bp)

    return app
