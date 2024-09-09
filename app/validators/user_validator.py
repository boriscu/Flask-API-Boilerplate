from app.validators.base_validator import BaseValidator


class UserValidator(BaseValidator):
    """
    A validator for user registration data, extending the BaseValidator.
    """

    @classmethod
    def validate_user_register_data(cls, data: dict) -> tuple[bool, str]:
        """
        Validate user registration data.

        Args:
            data (dict): The user data to be validated.

        Returns:
            tuple: A boolean indicating success, and a message with details.
        """
        validation_map = {
            "name": {"required": True, "type": str},
            "surname": {"required": True, "type": str},
            "email": {"required": True, "type": str},
            "password": {"required": True, "type": str},
        }
        return cls.validate_data(data, validation_map)

    @classmethod
    def validate_user_login_data(cls, data: dict) -> tuple[bool, str]:
        """
        Validate user login data.

        Args:
            data (dict): The user data to be validated.

        Returns:
            tuple: A boolean indicating success, and a message with details.
        """
        validation_map = {
            "email": {"required": True, "type": str},
            "password": {"required": True, "type": str},
        }
        return cls.validate_data(data, validation_map)
