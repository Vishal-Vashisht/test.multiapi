from flask import Flask, jsonify, Response
from config.redis_config import redis_client
from app.api.controllers.user_controller import auth_bp
from app.api.controllers.convert_type_controller import convert_bp
from app.api.controllers.traveler_controller import travler_bp
from app.api.models.models import db, migrate
# from app.api.models.models import TestCaseQuery
import json
import time
from flask_cors import CORS
from app.scheduler import regiset_scheduler


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.dev")
    # redis_client.init_app(app)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    regiset_scheduler(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(convert_bp)
    app.register_blueprint(travler_bp)
    return app
