from peewee import TextField, BlobField, BooleanField

from .base import BaseModel


class Workspace(BaseModel):

    name = TextField()
    description = TextField(default="")
    namespaces = TextField()
    icon_image = BlobField(null=True)
    is_personal = BooleanField(default=False, null=False)
