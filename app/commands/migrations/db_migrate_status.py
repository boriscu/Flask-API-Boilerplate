import click
from flask.cli import with_appcontext
from app.logger_setup import LoggerSetup
from app.db_init import router
from peewee_migrate import Migrator


@click.command(
    "db:migrate-status",
    help="This command is used to list all migrations and point out current migration status.",
)
@with_appcontext
def command():
    logger = LoggerSetup.get_logger("migrations")

    all_migrations = router.todo
    if len(router.done) != 0:
        last_migration = sorted(router.done)[len(router.done) - 1]
    else:
        last_migration = None

    logger.info("All migrations:")
    for migration in sorted(all_migrations):
        status = (
            "[DONE]" if last_migration and migration <= last_migration else "[TODO]"
        )

        if migration == last_migration:
            logger.info(f"{migration:60} {status:6} [*]")
        else:
            logger.info(f"{migration:60} {status:6}")
