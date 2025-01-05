from app.models.enums.http_status import HttpStatus


http_status_message_map = {
    HttpStatus.OK: "Success",
    HttpStatus.CREATED: "Resource created successfully",
    HttpStatus.ACCEPTED_FOR_PROCESSING: "Request accepted for processing",
    HttpStatus.NO_CONTENT: "No content",
    HttpStatus.BAD_REQUEST: "Bad request",
    HttpStatus.UNAUTHORIZED: "Unauthorized",
    HttpStatus.FORBIDDEN: "Forbidden",
    HttpStatus.NOT_FOUND: "Resource not found",
    HttpStatus.METHOD_NOT_ALLOWED: "Method not allowed",
    HttpStatus.NOT_ACCEPTABLE: "Not acceptable",
    HttpStatus.REQUEST_TIMEOUT: "Request timeout",
    HttpStatus.CONFLICT: "Conflict",
    HttpStatus.UNSUPPORTED_MEDIA_TYPE: "Unsupported media type",
    HttpStatus.UNPROCESSABLE_ENTITY: "Unprocessable entity",
    HttpStatus.RESOURCE_LOCKED: "Resource locked",
    HttpStatus.INTERNAL_SERVER_ERROR: "Internal server error",
    HttpStatus.SERVICE_UNAVAILABLE: "Service unavailable",
}
