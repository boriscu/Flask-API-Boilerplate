import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from config.app_config import AppConfig

from app.init.logger_setup import LoggerSetup
from app.models.pg.user_profile import UserProfile


@click.command(
    "seed:admin",
    help="This command is used to generate admin account based on configuration data.",
)
@with_appcontext
def seed_admin_command():
    logger = LoggerSetup.get_logger("cli")

    if UserProfile.select().where(UserProfile.is_admin == True).count() == 0:
        UserProfile.create(
            email=AppConfig.ADMIN_EMAIL,
            password=generate_password_hash(AppConfig.ADMIN_PASSWORD),
            name="Admin",
            surname="Admin",
            is_admin=True,
            is_active=True,
        )

        logger.info(f"Admin account seeded successfully.")
    else:
        logger.info(f"Admin account already exists.")
