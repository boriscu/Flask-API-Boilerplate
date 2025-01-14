from flask_restx import fields


def get_invite_creation_response_schema(namespace):
    invite_creation_response_schema = namespace.model(
        "Invite creation response",
        {
            "msg": fields.String(
                required=True,
                description="Response message indicating the outcome of the operation",
                example="Invite created successfully.",
            ),
            "workspace_id": fields.Integer(
                required=True,
                description="The unique identifier of the newly created invite",
                example=123,
            ),
        },
    )
    return invite_creation_response_schema
