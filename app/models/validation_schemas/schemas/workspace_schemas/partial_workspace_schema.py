from flask_restx import fields


def get_partial_workspace_schema(namespace):
    full_workspace_schema = namespace.model(
        "Partial workspace",
        {
            "name": fields.String(
                description="The name of the workspace.", example="University Workspace"
            ),
            "icon_image": fields.String(
                description="A binary string representing the compressed icon image for the workspace.",
                example="Base64 encoded PNG image data",
            ),
            "id": fields.Integer(
                description="A unique identifier for the workspace.", example=101
            ),
        },
    )
    return full_workspace_schema
