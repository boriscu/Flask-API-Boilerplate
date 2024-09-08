import click
from flask.cli import with_appcontext
from app.logger_setup import LoggerSetup
from app.db_init import router


@click.command("db:rollback", help="This command is used to rollback migrations.")
@click.option(
    "--steps",
    is_flag=False,
    default=1,
    help="[UNSTABLE] Number of migrations to rollback (defaults to 1).",
)
@with_appcontext
def command(steps):
    logger = LoggerSetup.get_logger("migrations")

    try:
        router.rollback()
        logger.info(f"Rolled back the last {steps} migration(s) successfully.")
    except Exception as exception:
        logger.error(f"There was an error while running last {steps} migration(s).")
        logger.error(exception)
