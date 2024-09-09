import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app.logger_setup import LoggerSetup
from app.models.user_profile import UserProfile
from config.app_config import AppConfig


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
        )

        logger.info(f"Admin account seeded successfully.")
    else:
        logger.info(f"Admin account already exists.")
