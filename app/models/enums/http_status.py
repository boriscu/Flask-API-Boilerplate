from enum import Enum


class HttpStatus(Enum):
    """
    Enum to map commonly used HTTP status codes to descriptive names.
    """

    OK = 200
    CREATED = 201
    ACCEPTED_FOR_PROCESSING = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    UNSUPPORTED_MEDIA_TYPE = 415
    UNPROCESSABLE_ENTITY = 422
    RESOURCE_LOCKED = 423
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
