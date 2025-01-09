from typing import Any, Dict, List, Optional, Tuple

from flask import Response, json
from flask_jwt_extended import get_jwt_identity

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile
from app.models.pg.workspace import Workspace

from app.helpers.http_response_generator import HttpResponseGenerator
from app.helpers.image_processor import ImageProcessor

from app.services.user_services.user_auth_service import UserAuthService
from app.services.workspace_services.workspace_pagination_service import (
    WorkspacePaginationService,
)


class WorkspaceCRUDService:
    @staticmethod
    def create_workspace(args: Dict[str, Any]) -> Response:
        """Create a new workspace in the database and return a Flask response object.

        Args:
            args (Dict[str, Any]): A dictionary containing workspace attributes.

        Returns:
            Response: Flask response object with the creation status and workspace ID.

        Raises:
            ValueError: If required attributes are missing or invalid.
        """
        UserAuthService.check_if_admin()

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

    @staticmethod
    def update_workspace(workspace_id: int, args: Dict[str, Any]) -> Response:
        """Update an existing workspace in the database and return a Flask response object.

        Args:
            workspace_id (int): The ID of the workspace to update.
            args (Dict[str, Any]): A dictionary containing workspace attributes.

        Returns:
            Response: Flask response object with the update status.

        Raises:
            ValueError: If required attributes are missing or invalid.
            NotFoundError: If the workspace with the given ID does not exist.
        """
        workspace = Workspace.get_by_id(workspace_id)

        workspace.name = args.get("name", workspace.name)
        workspace.description = args.get("description", workspace.description)
        workspace.namespaces = args.get("namespaces", workspace.namespaces)

        icon_image = args.get("icon_image", None)
        if icon_image:
            workspace.icon_image = ImageProcessor.compress_image(icon_image)

        workspace.save()

        return Response(
            f'{{"msg": "Workspace updated successfully.", "workspace_id": {workspace.id}}}',
            status=HttpStatus.OK.value,
            mimetype="application/json",
        )

    @staticmethod
    def get_all_workspaces(args: dict) -> Tuple[List[Workspace], int, int]:
        UserAuthService.check_if_admin()
        return WorkspacePaginationService.get_rows(
            page=args.get("page", 1),
            per_page=args.get("per_page", 10),
            sort_field=args.get("sort_field", "created_at"),
            sort_order=args.get("sort_order", "asc"),
            search=args.get("search", " "),
            filters=json.loads(args["filters"]) if args["filters"] else None,
        )

    @staticmethod
    def get_single_workspace(workspace_id: int) -> Optional[Workspace]:

        UserAuthService.check_if_admin()
        workspace = Workspace.get_by_id(workspace_id)

        if workspace.icon_image:
            encoded_image = ImageProcessor.encode_image(workspace.icon_image)
            workspace.icon_image = encoded_image

        return workspace

    @staticmethod
    def get_current_workspace() -> Optional[Workspace]:

        current_user = UserProfile.get_by_id(int(get_jwt_identity()))

        if current_user.workspace:
            workspace = current_user.workspace

            if workspace.icon_image:
                encoded_image = ImageProcessor.encode_image(workspace.icon_image)
                workspace.icon_image = encoded_image

        else:
            workspace = None

        return workspace

    @staticmethod
    def delete_workspace(workspace_id: int):
        UserAuthService.check_if_admin()

        Workspace.delete().where(Workspace.id == workspace_id).execute()

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
