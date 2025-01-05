from enum import Enum


class HttpStatus(Enum):
    """
    Enum to map commonly used HTTP status codes to descriptive names.
    """

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    CONFLICT = 409
    NO_CONTENT = 204
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    UNSUPPORTED_MEDIA_TYPE = 415
