import os

from .validator import Validator


class EmailPathToBodyValidator(Validator):
    def validate(self, path_to_body: str) -> str:
        if not os.path.exists(path_to_body):
            raise ValueError("Email body file does not exist.")

        if not path_to_body.endswith(".html"):
            raise ValueError("Email body must be a HTML file.")

        return path_to_body
