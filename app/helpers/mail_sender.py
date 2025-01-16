from flask import Flask
from flask_mail import Mail, Message

from app.helpers.validator.email_body_validator import EmailPathToBodyValidator
from app.helpers.validator.email_validator import EmailValidator
from config.app_config import AppConfig


class MailSender:
    _instance = None

    def __new__(cls, *args, **kwargs):
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
        self, recipients: str | list[str] | tuple, subject: str, path_to_body: str
    ) -> None:
        """
        Sends an email to the specified recipients with the given subject and body.

        :param recipients: Can be a single email or a list of emails.
        :param subject: The subject of the email.
        :param path_to_body: The body of the email.
        :return: None
        """

        recipients = EmailValidator().validate(recipients)
        path_to_body = EmailPathToBodyValidator().validate(path_to_body)

        message = Message(
            subject=subject, recipients=recipients, sender="radovic.nenad158@gmail.com"
        )

        with open(path_to_body, "r", encoding="utf-8") as file:
            message.body = file.read()

        self.mail.send(message)
