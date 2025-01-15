import re

from flask import Flask
from flask_mail import Mail, Message

from app.init.logger_setup import LoggerSetup
from config.app_config import AppConfig

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


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

        logger = LoggerSetup.get_logger("general")

        if not self._validate_email(recipients) and self._validate_body(path_to_body):
            return

        message = Message(
            subject=subject, recipients=recipients, sender="radovic.nenad158@gmail.com"
        )

        try:
            with open(path_to_body, "r", encoding="utf-8") as file:
                message.body = file.read()
        except Exception as e:
            logger.info("There was an error while reading email body.")
            logger.info(e)
            return

        try:
            logger.info("Trying to send email...")
            self.mail.send(message)
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.info("There was an error while sending email.")
            logger.info(e)

    def _validate_email(self, recipients: list[str]) -> bool:
        """
        Validates the email addresses in the given list.

        :param recipients: A list of email addresses to validate.
        :return: True if all addresses are valid, False otherwise.
        """
        logger = LoggerSetup.get_logger("general")
        for receiptient in recipients:
            if not re.match(EMAIL_REGEX, receiptient):
                logger.info(f"Invalid email address format: {receiptient}.")
                return False
        return True

    def _validate_body(self, path_to_body: str) -> bool:
        """
        Validates the body of the email by checking if the given path to the body ends with .html.

        :param path_to_body: The path to the body of the email.
        :return: True if the body is valid, False otherwise.
        """
        logger = LoggerSetup.get_logger("general")
        if not path_to_body.endswith(".html"):
            logger.info("Provided body must be of type .html.")
            return False
        return True
