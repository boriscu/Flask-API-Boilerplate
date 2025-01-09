from peewee import TextField, BooleanField, ForeignKeyField

from app.models.pg.workspace import Workspace

from .base import BaseModel


class UserProfile(BaseModel):
    name = TextField(null=False)
    surname = TextField(null=False)
    email = TextField(unique=True)
    password = TextField(null=False)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_sso = BooleanField(default=False)
    workspace = ForeignKeyField(Workspace, null=True, on_delete="SET NULL")
