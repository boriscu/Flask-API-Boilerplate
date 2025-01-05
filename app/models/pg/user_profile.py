from peewee import TextField, BooleanField

from .base import BaseModel


class UserProfile(BaseModel):
    name = TextField(null=False)
    surname = TextField(null=False)
    email = TextField(unique=True)
    password = TextField(null=False)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)
