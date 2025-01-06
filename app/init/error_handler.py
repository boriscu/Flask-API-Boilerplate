from flask import Flask
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from peewee import DoesNotExist, IntegrityError, PeeweeException
import sentry_sdk

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator


def register_error_handlers(app: Flask):
    """
    Automatically registers error handlers for all HTTP status codes in the HttpStatus enum.

    Args:
        app (Flask): The Flask application instance.
    """

    def generate_error_handler(status: HttpStatus):
        """
        Generates a Flask error handler for a specific HTTP status.

        Args:
            status (HttpStatus): The HTTP status for which to generate the handler.

        Returns:
            Callable: A Flask error handler function.
        """

        def handler(e):
            if status.value >= 500:
                sentry_sdk.capture_exception(e)
                log_message = (
                    f"Error {status.value}: {str(e)}, Type: {type(e).__name__}"
                )
                sentry_sdk.capture_message(log_message, level="error")
            elif status.value >= 400:
                sentry_sdk.capture_message(
                    f"Client error {status.value}: {str(e)}", level="warning"
                )

            return HttpResponseGenerator.generate_response(status)

        return handler

    for status in HttpStatus:
        if 400 <= status.value < 600:
            app.register_error_handler(status.value, generate_error_handler(status))

    @app.errorhandler(DoesNotExist)
    def handle_does_not_exist(e):
        """Handle Peewee DoesNotExist exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.NOT_FOUND)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        """Handle Peewee IntegrityError exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.BAD_REQUEST)

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        """Handle Peewee ValueError exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.BAD_REQUEST)

    @app.errorhandler(PeeweeException)
    def handle_peewee_exception(e):
        """Handle general Peewee exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.BAD_REQUEST)

    @app.errorhandler(PermissionError)
    def handle_permission_exception(e):
        """Handle PermissionError exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.FORBIDDEN)

    @app.errorhandler(RuntimeError)
    def handle_runtime_exception(e):
        """Handle RuntimeError exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.INTERNAL_SERVER_ERROR)

    @app.errorhandler(KeyError)
    def handle_key_exception(e):
        """Handle KeyError exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.BAD_REQUEST)

    @app.errorhandler(TypeError)
    def handle_type_exception(e):
        """Handle TypeError exceptions."""
        sentry_sdk.capture_message(e)
        return HttpResponseGenerator.generate_response(HttpStatus.BAD_REQUEST)

    @app.errorhandler(IndexError)
    def handle_index_exception(e):
        """Handle IndexError exceptions."""
        sentry_sdk.capture_exception(e)
        return HttpResponseGenerator.generate_response(HttpStatus.INTERNAL_SERVER_ERROR)

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """
        Handle general exceptions not specifically mapped to an HTTP status.
        Defaults to INTERNAL_SERVER_ERROR.
        """
        sentry_sdk.capture_exception(e)
        return HttpResponseGenerator.generate_response(HttpStatus.INTERNAL_SERVER_ERROR)

    @app.before_request
    def before_request_func():
        try:
            verify_jwt_in_request()
            jwt_data = get_jwt()
            if jwt_data:
                sentry_sdk.set_user({"id": get_jwt_identity()})
        except:
            pass
