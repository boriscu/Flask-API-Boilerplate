import click

from app.init.logger_setup import LoggerSetup

from app.helpers.email.strategies.test_mail_sender import TestMailSender


@click.command("mail:send", help="This command is used to send an email.")
@click.option(
    "--to",
    multiple=True,
    required=True,
    help="The recipient's email address. This option can be specified multiple times for multiple recipients.",
)
@click.option(
    "--name",
    type=str,
    required=True,
    help="The sender's email address that appears in the 'From' field.",
)
@click.option(
    "--subject", type=str, required=True, help="The subject line of the email."
)
def command(to: tuple, subject: str, name: str) -> None:

    logger = LoggerSetup.get_logger("cli")

    try:
        logger.info("Trying to send email...")
        TestMailSender().send_template(
            recipients=to,
            subject=subject,
            name=name,
        )
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.info("There was an error while sending email.")
        logger.info(e)
