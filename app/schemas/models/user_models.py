from flask_restx import fields


def create_user_models(namespace):
    user_registration_model = namespace.model(
        "UserRegistration",
        {
            "name": fields.String(required=True, description="First name of the user"),
            "surname": fields.String(required=True, description="Surname of the user"),
            "email": fields.String(
                required=True, description="Email address of the user"
            ),
            "password": fields.String(
                required=True, description="Password for account creation"
            ),
        },
    )

    user_login_model = namespace.model(
        "UserLogin",
        {
            "email": fields.String(required=True, description="User email address"),
            "password": fields.String(required=True, description="User password"),
        },
    )

    user_profile_model = namespace.model(
        "UserProfile",
        {
            "name": fields.String(description="First name of the user"),
            "surname": fields.String(description="Surname of the user"),
            "email": fields.String(description="Email address of the user"),
            "is_admin": fields.Boolean(
                description="Flag noting if the user has the admin role"
            ),
        },
    )

    return {
        "registration": user_registration_model,
        "login": user_login_model,
        "profile": user_profile_model,
    }
