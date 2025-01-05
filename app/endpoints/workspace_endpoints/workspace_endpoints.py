from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/", methods=["POST"])
class CreateWorkspace(Resource):
    @workspace_namespace.doc(
        description="Creates a workspace. Requires admin privileges."
    )
    @jwt_required()
    @workspace_namespace.expect(
        workspace_schema_retriever.retrieve("file_upload_parser")
    )
    @workspace_namespace.response(
        HttpStatus.CREATED.value,
        "Resource created successfully",
    )
    def post(self):
        args = workspace_schema_retriever.retrieve("file_upload_parser").parse_args()

        name = args["name"]
        description = args["description"]
        namespaces = args["namespaces"]
        icon_image = args["icon_image"]

        return HttpResponseGenerator.generate_response(HttpStatus.CREATED)
