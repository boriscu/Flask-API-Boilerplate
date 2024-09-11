from flask_restx import fields

login_model = (
    "UserLogin",
    {
        "email": fields.String(
            required=True,
            description="User email address",
            example="john.doe@mail.com",
        ),
        "password": fields.String(
            required=True, description="User password", example="Strong password"
        ),
    },
)
