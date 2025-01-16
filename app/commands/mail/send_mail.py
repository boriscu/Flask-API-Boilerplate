import click

from flask import current_app

from app.init.logger_setup import LoggerSetup

from app.helpers.mail_sender import MailSender


@click.command("mail:send", help="This command is used to send an email.")
@click.option(
    "--to",
    multiple=True,
    required=True,
)
@click.option("--subject", type=str, required=True)
@click.option(
    "--body",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
)
def command(to: tuple, subject: str, body: str) -> None:
    logger = LoggerSetup.get_logger("cli")

    try:
        logger.info("Trying to send email...")
        MailSender(current_app).send_email(
            recipients=to, subject=subject, path_to_body=body
        )
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.info("There was an error while sending email.")
        logger.info(e)
