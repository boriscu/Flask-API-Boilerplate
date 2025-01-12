from flask_restx import fields


def get_create_workspace_response_schema(namespace):
    create_workspace_response_schema = namespace.model(
        "WorkspaceCreationResponse",
        {
            "msg": fields.String(
                required=True,
                description="Response message indicating the outcome of the operation",
                example="Workspace created successfully.",
            ),
            "workspace_id": fields.Integer(
                required=True,
                description="The unique identifier of the newly created workspace",
                example=123,
            ),
        },
    )
    return create_workspace_response_schema
