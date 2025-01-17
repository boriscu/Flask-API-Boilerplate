from peewee import BlobField, IntegerField, TextField

from app.models.enums.workspace_type import WorkspaceType

from .base import BaseModel


class Workspace(BaseModel):
    name = TextField()
    description = TextField(default="")
    namespaces = TextField()
    icon_image = BlobField(null=True)
    workspace_type = IntegerField(default=WorkspaceType.REGULAR.value, null=False)
    user_limit = IntegerField(default=10, null=False)
