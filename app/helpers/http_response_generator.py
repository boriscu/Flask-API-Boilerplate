from typing import Tuple
from flask import jsonify, Response

from app.models.maps.http_status_message_map import http_status_message_map

from app.models.enums.http_status import HttpStatus


class HttpResponseGenerator:
    @staticmethod
    def generate_response(status: HttpStatus) -> Tuple[str, int]:
        """
        Generates a JSON response with a message corresponding to a given HTTP status code.

        Args:
            status (HTTPStatus): An HTTPStatus enum value representing the HTTP status code.

        Returns:
            Tuple[str, int]: A tuple containing the JSON response and the integer value of the HTTP status.
        """

        message = http_status_message_map.get(status, "An unknown error occurred")
        return Response(
            f'{{"msg": "{message}"}}',
            status=status.value,
            mimetype="application/json",
        )
