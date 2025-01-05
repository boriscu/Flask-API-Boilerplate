import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from config.app_config import AppConfig

from app.models.enums.app_environment import AppEnvironment


class SentryInitializer:
    @classmethod
    def get_parsed_sentry_env(cls):
        environment_map = {
            AppEnvironment.DEV.value: "development",
            AppEnvironment.STAGING.value: "staging",
            AppEnvironment.PROD.value: "production",
        }

        return environment_map.get(AppConfig.APP_ENVIRONMENT)

    @classmethod
    def initialize(cls):
        """Initialize Sentry SDK with the provided configuration."""

        sentry_sdk.init(
            dsn=AppConfig.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            send_default_pii=True,
            attach_stacktrace=True,
            max_request_body_size="always",
            environment=cls.get_parsed_sentry_env(),
            _experiments={
                "continuous_profiling_auto_start": True,
            },
        )
