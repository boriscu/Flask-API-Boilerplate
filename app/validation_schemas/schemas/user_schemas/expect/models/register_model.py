from flask_restx import fields

register_model = (
    "UserRegistration",
    {
        "name": fields.String(
            required=True, description="First name of the user", example="John"
        ),
        "surname": fields.String(
            required=True, description="Surname of the user", example="Doe"
        ),
        "email": fields.String(
            required=True,
            description="Email address of the user, must be unique",
            example="john.doe@mail.com",
        ),
        "password": fields.String(
            required=True,
            description="Password for account creation",
            example="Strong password",
        ),
    },
)
