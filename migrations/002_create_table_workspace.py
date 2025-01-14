"""Peewee migrations -- 002_create_table_workspace.py.

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

from app.models.enums.workspace_type import WorkspaceType

from app.models.pg.base import BaseModel


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    @migrator.create_model
    class Workspace(BaseModel):
        id = pw.AutoField()
        name = pw.TextField(null=False)
        description = pw.TextField(default="")
        namespaces = pw.TextField(default="[]")
        icon_image = pw.BlobField(null=True)
        workspace_type = pw.IntegerField(
            default=WorkspaceType.REGULAR.value, null=False
        )
        user_limit = pw.IntegerField(default=10, null=False)


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.drop_table("workspace")
