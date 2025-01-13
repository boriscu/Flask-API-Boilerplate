import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from app.init.logger_setup import LoggerSetup

from config.app_config import AppConfig

from app.models.enums.workspace_type import WorkspaceType
from app.models.enums.workspace_user_role import WorkspaceUserRole

from app.models.pg.workspace import Workspace
from app.models.pg.workspace_user import WorkspaceUser
from app.models.pg.user_profile import UserProfile


@click.command(
    "seed:admin",
    help="This command is used to generate admin account based on configuration data.",
)
@with_appcontext
def seed_admin_command():
    logger = LoggerSetup.get_logger("cli")

    if UserProfile.select().where(UserProfile.is_admin == True).count() == 0:
        new_user = UserProfile.create(
            email=AppConfig.ADMIN_EMAIL,
            password=generate_password_hash(AppConfig.ADMIN_PASSWORD),
            name="Admin",
            surname="Admin",
            is_admin=True,
            is_active=True,
            workspace_creation_quota=None,
        )

        new_workspace = Workspace.create(
            name="Admins' Workspace",
            description="Workspace that belongs to the admin",
            namespaces="[]",
            icon_image=None,
            workspace_type=WorkspaceType.PERSONAL.value,
        )

        WorkspaceUser.create(
            user_id=new_user.id,
            workspace_id=new_workspace.id,
            workspace_user_role=WorkspaceUserRole.ADMIN.value,
        )

        logger.info(f"Admin account seeded successfully.")
    else:
        logger.info(f"Admin account already exists.")
