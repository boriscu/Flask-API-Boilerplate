import re

from flask import Flask, current_app
from flask_mail import Mail, Message

from config.app_config import AppConfig


class MailSender:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(MailSender, cls).__new__(cls)
        return cls._instance

    def __init__(self, app: Flask = current_app):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.app = app

            # TODO: Replace sender.
            app.config["MAIL_SERVER"] = AppConfig.MAIL_SERVER
            app.config["MAIL_PORT"] = AppConfig.MAIL_PORT
            app.config["MAIL_USERNAME"] = AppConfig.MAIL_USERNAME
            app.config["MAIL_PASSWORD"] = AppConfig.MAIL_PASSWORD
            app.config["MAIL_DEFAULT_SENDER"] = "radovic.nenad158@gmail.com"
            app.config["MAIL_USE_TLS"] = True
            app.config["MAIL_USE_SSL"] = False

            self.mail = Mail(app)

    def send_html(self, recipients: list[str] | str, subject: str, html: str) -> None:
        """
        Sends an HTML email to the specified recipients with the given subject and HTML content.

        :param recipients: Can be a single email address or a list of email addresses.
        :param subject: The subject line of the email.
        :param html: The HTML content to be sent as the body of the email.
        :return: None
        """

        if isinstance(recipients, str):
            recipients = [recipients]

        if not self._validate_email(recipients):
            return

        message = Message(
            subject=subject,
            recipients=recipients,
            html=html,
        )

        return self.mail.send(message)

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
