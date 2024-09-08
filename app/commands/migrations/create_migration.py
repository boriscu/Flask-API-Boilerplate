import click
from flask.cli import with_appcontext
from app.logger_setup import LoggerSetup
from app.db_init import router


@click.command(
    "db:create-migration", help="This command is used to create new migration file."
)
@click.option(
    "--name",
    is_flag=False,
    help="Provide name of the migration file that you want to create.",
)
@click.option(
    "--auto",
    is_flag=True,
    help="[UNSTABLE] Autogenerate migration based on recent changes. Useful to bootstrap the process of writing migrations but ALWAYS check the generated code!",
)
@with_appcontext
def command(name, auto):
    logger = LoggerSetup.get_logger("migrations")

    try:
        router.create(name, auto=auto)
        logger.info(f"Migration {name} created successfully.")
    except Exception as exception:
        logger.error(f"There was an error while creating migration file.")
        logger.error(exception)
