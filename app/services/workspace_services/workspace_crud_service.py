from typing import Any, Dict

from flask import Response, jsonify

from app.models.enums.http_status import HttpStatus

from app.models.pg.workspace import Workspace

from app.helpers.image_processor import ImageProcessor


class WorkspaceCRUDService:
    @classmethod
    def create_workspace(cls, args: Dict[str, Any]) -> Response:
        """Create a new workspace in the database and return a Flask response object.

        Args:
            args (Dict[str, Any]): A dictionary containing workspace attributes.

        Returns:
            Response: Flask response object with the creation status and workspace ID.

        Raises:
            ValueError: If required attributes are missing or invalid.
        """
        name = args.get("name")
        description = args.get("description", "")
        namespaces = args.get("namespaces", "[]")
        icon_image = args.get("icon_image", None)
        icon_data = ImageProcessor.compress_image(icon_image) if icon_image else None

        new_workspace = Workspace.create(
            name=name,
            description=description,
            namespaces=namespaces,
            icon_image=icon_data,
        )

        return Response(
            f'{{"msg": "Workspace created successfully.", "workspace_id": {new_workspace.id}}}',
            status=HttpStatus.CREATED.value,
            mimetype="application/json",
        )
