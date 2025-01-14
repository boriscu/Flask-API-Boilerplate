import re

import click
from flask import Flask, current_app
from flask_mail import Mail, Message

from config.app_config import AppConfig

# Define a regex pattern for validating email addresses
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


def validate_email(ctx, param, value: str) -> str:
    if not re.match(EMAIL_REGEX, value):
        raise click.BadParameter("Invalid email address format.")
    return value


def validate_body(ctx, param, value: click.Path) -> click.Path:
    if not value.endswith(".html"):
        raise click.BadParameter("Body must be of type .html.")
    return value


@click.command("mail:send", help="This command is used to send an email.")
@click.argument(
    "email",
    type=click.STRING,
    callback=validate_email,
    required=True,
)
@click.argument(
    "path_to_body",
    type=click.Path(exists=True, dir_okay=False),
    callback=validate_body,
    required=True,
)
def command(email: str, path_to_body: str) -> None:
    with open(path_to_body, "r", encoding="utf-8") as file:
        body = file.read()

    mail = get_mail_object()
    message: Message = Message(
        subject="Welcome, user!",
        recipients=[email],
        sender="radovic.nenad158@gmail.com",
    )
    message.body = body
    mail.send(message)
