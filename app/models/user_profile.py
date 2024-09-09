from peewee import TextField

from .base import BaseModel


class UserProfile(BaseModel):
    name = TextField(null=False)
    surname = TextField(null=False)
    email = TextField(unique=True)
    password = TextField(null=False)
    is_admin = TextField(default=False)
