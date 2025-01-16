import re

from .validator import Validator


class EmailValidator(Validator):
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate(self, emails: str | list[str] | tuple) -> list[str]:
        if isinstance(emails, str) or isinstance(emails, tuple):
            emails = list(emails)

        for email in emails:
            if not re.match(self.EMAIL_REGEX, email):
                raise ValueError(f"Invalid email address - {email}.")

        return emails
