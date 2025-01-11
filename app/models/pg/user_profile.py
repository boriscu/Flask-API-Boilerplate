from peewee import (
    TextField,
    BooleanField,
    DateField,
    CharField,
    BlobField,
)

from app.models.pg.workspace import Workspace

from .base import BaseModel


class UserProfile(BaseModel):
    name = TextField(null=False)
    surname = TextField(null=False)
    email = TextField(unique=True)
    password = TextField(null=False)
    birthday = DateField(null=True)
    sex = CharField(null=True)
    profession = TextField(null=True)
    profile_picture = BlobField(null=True)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_sso = BooleanField(default=False)
