from peewee import TextField, BlobField

from .base import BaseModel


class Workspace(BaseModel):

    name = TextField()
    description = TextField(default="")
    namespaces = TextField()
    icon_image = BlobField(null=True)
