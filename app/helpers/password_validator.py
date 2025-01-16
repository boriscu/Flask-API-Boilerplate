import re


class PasswordValidator:
    @staticmethod
    def validate_password(password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character.")

        return password
