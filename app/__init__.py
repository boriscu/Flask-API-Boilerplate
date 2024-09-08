import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import redis

from app import routes
from app.commands import register_commands

from .services.celery_service import CeleryService
from config.app_config import AppConfig

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def create_app():
    app = Flask(__name__)

    AppConfig.load_config()

    app.config.from_object(AppConfig)

    cors = CORS(
        app,
        resources={r"/*": {"origins": AppConfig.ALLOWED_ORIGINS}},
        supports_credentials=True,
    )

    routes.init_app_routes(app)

    app.celery_client = CeleryService.celery_init_app(app)

    app.redis = redis.Redis(
        host=AppConfig.REDIS_HOST,
        port=AppConfig.REDIS_PORT,
        db=AppConfig.REDIS_DB,
        password=AppConfig.REDIS_PASSWORD,
    )

    register_commands(app)

    return app
