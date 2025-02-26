import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import redis

from app import routes

from config.app_config import AppConfig


from app.commands import register_commands

from app.init.before_handler import register_before_handlers
from app.init.sentry_init import SentryInitializer

from app.services.celery_service import CeleryService

from app.helpers.pre_request.pre_request_registrer import PreRequestRegistrer

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def create_app():
    app = Flask(__name__)

    app.app_context().push()

    AppConfig.load_config()

    SentryInitializer.initialize()

    app.config.from_object(AppConfig)

    cors = CORS(
        app,
        resources={r"/api/v1/*": {"origins": AppConfig.ALLOWED_ORIGINS}},
    )

    routes.init_app_routes(app)

    app.celery_client = CeleryService.celery_init_app(app)

    app.redis = redis.Redis(
        host=AppConfig.REDIS_HOST,
        port=AppConfig.REDIS_PORT,
        db=AppConfig.REDIS_DB,
        password=AppConfig.REDIS_PASSWORD,
    )

    PreRequestRegistrer(app).register_all()

    register_commands(app)
    register_before_handlers(app)

    return app
