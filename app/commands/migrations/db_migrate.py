import click
from flask.cli import with_appcontext
from app.logger_setup import LoggerSetup
from app.db_init import router


@click.command("db:migrate", help="This command is used to run migrations.")
@click.option(
    "--single",
    is_flag=True,
    help="Migrate only to the next migration instead of migrating all the way",
)
@with_appcontext
def command(single):
    logger = LoggerSetup.get_logger("migrations")

    try:
        diff = router.diff
        if not diff:
            logger.info("There is nothing to migrate.")
            return
        if single:
            router.run_one(name=diff[0], migrator=router.migrator, fake=False)
            logger.info(f"Migration {diff[0]} applied successfully.")
        else:
            router.run()
            logger.info(f"All migrations applied successfully.")
    except Exception as exception:
        logger.error(f"There was an error while running migrations.")
        logger.error(exception)
