import re

import click
from flask import Flask, current_app
from flask_mail import Mail, Message

from app.init.logger_setup import LoggerSetup
from config.app_config import AppConfig

# A regex pattern for validating email addresses
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

_mail: Mail | None = None


def get_mail_object() -> Mail:
    global _mail
    if _mail is None:
        _mail = Mail(current_app)
    return _mail


def initialize_email_client() -> None:
    app: Flask = current_app

    with app.app_context():
        app.config["MAIL_SERVER"] = AppConfig.MAIL_SERVER
        app.config["MAIL_PORT"] = AppConfig.MAIL_PORT
        app.config["MAIL_USERNAME"] = AppConfig.MAIL_USERNAME
        app.config["MAIL_PASSWORD"] = AppConfig.MAIL_PASSWORD
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USE_SSL"] = False


def validate_recipients(ctx, param, to: tuple) -> str:
    for receiptient in to:
        if not re.match(EMAIL_REGEX, receiptient):
            raise click.BadParameter("Invalid email address format.")
    return to


def validate_body(ctx, param, body: click.Path) -> click.Path:
    if not body.endswith(".html"):
        raise click.BadParameter("Body must be of type .html.")
    return body


@click.command("mail:send", help="This command is used to send an email.")
@click.option(
    "--to",
    multiple=True,
    callback=validate_recipients,
    required=True,
)
@click.option("--subject", type=str, required=True)
@click.option(
    "--body",
    type=click.Path(exists=True, dir_okay=False),
    callback=validate_body,
    required=True,
)
def command(to: tuple, subject: str, body: str) -> None:
    logger = LoggerSetup.get_logger("cli")

    try:
        with open(body, "r", encoding="utf-8") as file:
            body = file.read()
    except Exception as e:
        logger.info("There was an error while reading email body.")
        logger.info(e)
        return

    mail = get_mail_object()
    message: Message = Message(
        subject=subject,
        recipients=to,
        sender="radovic.nenad158@gmail.com",
    )
    message.body = body
    try:
        logger.info("Trying to send email...")
        mail.send(message)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.info("There was an error while sending email.")
        logger.info(e)
