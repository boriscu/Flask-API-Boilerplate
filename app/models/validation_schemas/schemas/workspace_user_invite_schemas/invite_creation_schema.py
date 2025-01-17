from flask_restx import fields

from app.models.enums.workspace_user_role import WorkspaceUserRole


def get_invite_creation_schema(namespace):
    invite_creation_schema = namespace.model(
        "Workspace invite",
        {
            "user_email": fields.String(
                description="A user email address.",
                example="example@uns.ac.rs",
            ),
            "workspace_user_role": fields.Integer(
                description="A role that the user will have on the workspace.",
                example=1,
                enum=[WorkspaceUserRole.VIEW.value, WorkspaceUserRole.EDIT.value],
            ),
        },
    )
    return invite_creation_schema
