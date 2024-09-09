import os
from config.base_config import BaseConfig


class AppConfig(BaseConfig):
    """
    Application-specific configuration class that handles environment variables for the application.
    Inherits from BaseConfig and loads configurations directly from environment variables.
    """

    # Celery Jobs
    CELERY_BROKER_URL = None
    CELERY_RESULT_BACKEND = None

    # CORS allowed origins
    ALLOWED_ORIGINS = [
        "http://localhost:3000",  # Development origin
    ]

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = 0
    REDIS_PASSWORD = None
    REDIS_URL = None

    # File path config
    TEMP_STORAGE_PATH = "storage/temp"

    # Database
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)

    # Token and cookies
    JWT_SECRET_KEY = None
    JWT_TOKEN_LOCATION = None

    # Additional security configurations
    COOKIE_SECURE = None
    CSRF_PROTECT = None
    WTF_CSRF_ENABLED = None
    JWT_COOKIE_CSRF_PROTECT = None
    HTTP_ONLY = None
    COOKIE_DOMAIN = None
    COOKIE_PATH = None
    DEBUG_MODE = None

    # Admin seeding
    ADMIN_EMAIL = None
    ADMIN_PASSWORD = None

    @classmethod
    def load_config(cls):
        """
        Loads environment variable-based configurations.
        Populates the class attributes with the configuration data.
        """
        if cls._are_attributes_none():

            cls.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
            cls.JWT_TOKEN_LOCATION = ["cookies"]

            cls.COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False") == "True"
            cls.CSRF_PROTECT = os.getenv("CSRF_PROTECT", "False") == "True"
            cls.WTF_CSRF_ENABLED = os.getenv("CSRF_PROTECT", "False") == "True"
            cls.JWT_COOKIE_CSRF_PROTECT = os.getenv("CSRF_PROTECT", "False") == "True"
            cls.HTTP_ONLY = os.getenv("HTTP_ONLY", "False") == "True"
            cls.COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN")
            cls.COOKIE_PATH = os.getenv("COOKIE_PATH")
            cls.DEBUG_MODE = os.getenv("DEBUG_MODE")

            cls.REDIS_HOST = os.getenv("REDIS_HOST")
            cls.REDIS_PORT = os.getenv("REDIS_PORT")
            cls.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
            cls.REDIS_URL = f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"

            cls.CELERY_BROKER_URL = cls.REDIS_URL
            cls.CELERY_RESULT_BACKEND = cls.REDIS_URL

            cls.ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
            cls.ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

        super().check_none_values()

    @classmethod
    def _are_attributes_none(cls):
        """
        Checks if any of the class attributes are None.
        Returns True if any attribute is None, otherwise False.
        """
        for key in cls.__dict__:
            if not key.startswith("__") and not callable(getattr(cls, key)):
                if getattr(cls, key) is None:
                    return True
        return False
