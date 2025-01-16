import re

from flask import Flask
from flask_mail import Mail, Message

from config.app_config import AppConfig


class MailSender:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(MailSender, cls).__new__(cls)
        return cls._instance

    def __init__(self, app: Flask):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.app = app
            self.mail = Mail(app)

            app.config["MAIL_SERVER"] = AppConfig.MAIL_SERVER
            app.config["MAIL_PORT"] = AppConfig.MAIL_PORT
            app.config["MAIL_USERNAME"] = AppConfig.MAIL_USERNAME
            app.config["MAIL_PASSWORD"] = AppConfig.MAIL_PASSWORD
            app.config["MAIL_USE_TLS"] = True
            app.config["MAIL_USE_SSL"] = False

    # TODO: Replace sender.
    def send_email(
        self, recipients: list[str] | str, subject: str, path_to_body: str
    ) -> None:
        """
        Sends an email to the specified recipients with the given subject and body.

        :param recipients: Can be a single email or a list of emails.
        :param subject: The subject of the email.
        :param path_to_body: The body of the email.
        :return: None
        """
        if isinstance(recipients, str):
            recipients = [recipients]

        if not self._validate_email(recipients) and self._validate_body(path_to_body):
            return

        message = Message(
            subject=subject, recipients=recipients, sender="radovic.nenad158@gmail.com"
        )

        with open(path_to_body, "r", encoding="utf-8") as file:
            message.body = file.read()

        self.mail.send(message)

    def get_email_regex(self) -> str:
        """
        Retrieves a regex pattern that matches valid email addresses.

        This regex pattern checks for emails that start with alphanumeric characters
        (including dots, underscores, percent signs, plus signs, and hyphens),
        followed by an '@' symbol, then more alphanumeric characters (including dots and hyphens),
        and finally ends with a dot followed by two or more alphabetic characters.

        Returns:
            str: A regex pattern for validating email addresses.
        """
        return r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def _validate_email(self, recipients: list[str]) -> bool:
        """
        Validates the email addresses in the given list.

        :param recipients: A list of email addresses to validate.
        :return: True if all addresses are valid, False otherwise.
        """
        for receiptient in recipients:
            if not re.match(self.get_email_regex(), receiptient):
                return False
        return True

    def _validate_body(self, path_to_body: str) -> bool:
        """
        Validates the body of the email by checking if the given path to the body ends with .html.

        :param path_to_body: The path to the body of the email.
        :return: True if the body is valid, False otherwise.
        """
        if not path_to_body.endswith(".html"):
            return False
        return True
