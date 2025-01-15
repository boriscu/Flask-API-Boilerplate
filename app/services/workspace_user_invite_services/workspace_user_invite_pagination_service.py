from typing import Any, Dict, List, Tuple

from flask import json
from flask_jwt_extended import get_jwt_identity
from app.helpers.image_processor import ImageProcessor
from app.models.pg.user_profile import UserProfile
from app.models.pg.workspace import Workspace
from app.models.pg.workspace_user_invite import WorkspaceUserInvite
from app.services.base_crud_services.base_pagination_service import (
    BasePaginationService,
)


class WorkspaceUserInvitePaginationService(BasePaginationService):
    @classmethod
    def get_user_accessible_rows(
        cls,
        user_id: int,
        page: int,
        per_page: int,
        sort_field: str,
        sort_order: str,
        search: str,
        filters: Dict[str, Any],
    ) -> Tuple[List[WorkspaceUserInvite], int, int]:
        query = (
            WorkspaceUserInvite.select(WorkspaceUserInvite, Workspace, UserProfile)
            .join(Workspace, on=(WorkspaceUserInvite.workspace == Workspace.id))
            .switch(WorkspaceUserInvite)
            .join(UserProfile, on=(WorkspaceUserInvite.user == UserProfile.id))
            .where(WorkspaceUserInvite.user == user_id)
        )
        query = cls.filter_query(query, WorkspaceUserInvite, filters)
        query = cls.search_query(query, WorkspaceUserInvite, search)

        total_entries = query.count()

        query = cls.sort_query(query, WorkspaceUserInvite, sort_field, sort_order)

        models_list = cls.paginate_query(query, page, per_page)

        total_pages = (total_entries + per_page - 1) // per_page

        return (models_list, total_entries, total_pages)

    @classmethod
    def get_serialized_invites(cls, args: dict):
        invitor_id = int(get_jwt_identity())
        invites, total_entries, total_pages = cls.get_user_accessible_rows(
            user_id=invitor_id,
            page=args.get("page", 1),
            per_page=args.get("per_page", 10),
            sort_field=args.get("sort_field", "created_at"),
            sort_order=args.get("sort_order", "asc"),
            search=args.get("search", " "),
            filters=json.loads(args["filters"]) if args["filters"] else None,
        )

        result = []
        for invite in invites:
            user_profile = invite.user
            workspace = invite.workspace
            encoded_profile_picture = ImageProcessor.encode_image(
                user_profile.profile_picture
            )
            encoded_icon_image = ImageProcessor.encode_image(workspace.icon_image)

            invite_data = {
                "workspace": {
                    "name": workspace.name,
                    "icon_image": encoded_icon_image,
                    "id": workspace.id,
                },
                "invitor": {
                    "name": user_profile.name,
                    "surname": user_profile.surname,
                    "email": user_profile.email,
                    "profile_picture": encoded_profile_picture,
                    "id": user_profile.id,
                },
                "invite_status": invite.invite_status,
                "workspace_user_role": invite.workspace_user_role,
                "created_at": invite.created_at,
                "id": invite.id,
            }
            result.append(invite_data)

        return result, total_entries, total_pages
