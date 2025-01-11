from peewee import ForeignKeyField

from app.models.pg.base import BaseModel
from app.models.pg.user_profile import UserProfile
from app.models.pg.workspace import Workspace


class WorkspaceUserProfile(BaseModel):
    workspace = ForeignKeyField(Workspace, null=False, on_delete="CASCADE")
    user_profile = ForeignKeyField(UserProfile, null=False, on_delete="CASCADE")
