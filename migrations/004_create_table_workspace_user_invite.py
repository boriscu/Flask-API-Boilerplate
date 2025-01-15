"""Peewee migrations -- 003_create_table_workspace_user_invite.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator

from app.models.enums.workspace_user_role import WorkspaceUserRole

from app.models.pg.base import BaseModel
from app.models.pg.user_profile import UserProfile
from app.models.pg.workspace import Workspace


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    @migrator.create_model
    class WorkspaceUserInvite(BaseModel):
        id = pw.AutoField()
        workspace = pw.ForeignKeyField(Workspace, null=False, on_delete="CASCADE")
        user = pw.ForeignKeyField(UserProfile, null=False, on_delete="CASCADE")
        workspace_user_role = pw.IntegerField(default=WorkspaceUserRole.VIEW.value)


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.drop_table("workspaceuserinvite")
