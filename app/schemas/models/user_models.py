from flask_restx import fields


def create_user_models(namespace):
    user_registration_model = namespace.model(
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

    user_login_model = namespace.model(
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

    user_profile_model = namespace.model(
        "UserProfile",
        {
            "name": fields.String(description="First name of the user", example="John"),
            "surname": fields.String(description="Surname of the user", example="Doe"),
            "email": fields.String(
                description="Email address of the user", example="john.doe@mail.com"
            ),
            "is_admin": fields.Boolean(
                description="Flag noting if the user has the admin role", example=False
            ),
        },
    )

    return {
        "registration": user_registration_model,
        "login": user_login_model,
        "profile": user_profile_model,
    }
