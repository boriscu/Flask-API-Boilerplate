from flask_restx import fields


def get_verification_response_schema(namespace):
    verification_respnose_schema = namespace.model(
        "Verification response",
        {
            "msg": fields.String(
                required=True,
                description="Response message",
                example="Login successful",
            ),
            "access_token": fields.String(
                required=True,
                description="JWT Token for the user that needs to be used for authentication",
                example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            ),
        },
    )
    return verification_respnose_schema
