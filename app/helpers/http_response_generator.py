from flask import Response

from app.models.maps.http_status_message_map import http_status_message_map

from app.models.enums.http_status import HttpStatus


class HttpResponseGenerator:
    @staticmethod
    def generate_response(status: HttpStatus) -> Response:
        """
        Generates a JSON response with a message corresponding to a given HTTP status code.

        Args:
            status (HttpStatus): An enum value of HttpStatus representing the HTTP status code.

        Returns:
            Response: A Flask Response object containing the JSON-formatted message and the HTTP status code.
        """

        message = http_status_message_map.get(status, "An unknown error occurred")
        return Response(
            f'{{"msg": "{message}"}}',
            status=status.value,
            mimetype="application/json",
        )
