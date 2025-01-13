import ast
from typing import Any, Dict, List, Tuple

from app.models.enums.workspace_type import WorkspaceType
from app.models.pg.workspace import Workspace
from app.models.pg.workspace_user import WorkspaceUser

from app.services.base_crud_services.base_pagination_service import (
    BasePaginationService,
)
from app.services.user_services.user_validation_service import UserValidationService


class WorkspacePaginationService(BasePaginationService):
    @classmethod
    def get_rows(
        cls,
        page: int,
        per_page: int,
        sort_field: str,
        sort_order: str,
        search: str,
        filters: Dict[str, Any],
    ) -> Tuple[List[Workspace], int, int]:
        return super().get_rows(
            Workspace, page, per_page, sort_field, sort_order, search, filters
        )

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
    ) -> Tuple[List[Workspace], int, int]:
        query = (
            Workspace.select().join(WorkspaceUser).where(WorkspaceUser.user == user_id)
        )
        query = cls.filter_query(query, Workspace, filters)
        query = cls.search_query(query, Workspace, search)

        total_entries = query.count()

        query = cls.sort_query(query, Workspace, sort_field, sort_order)

        models_list = cls.paginate_query(query, page, per_page)

        total_pages = (total_entries + per_page - 1) // per_page

        return (models_list, total_entries, total_pages)

    @classmethod
    def get_public_workspaces(
        cls,
        user_id: int,
        page: int,
        per_page: int,
        sort_field: str,
        sort_order: str,
        search: str,
        filters: Dict[str, Any],
    ) -> Tuple[List[Workspace], int, int]:

        query = Workspace.select().where(
            (Workspace.workspace_type == WorkspaceType.PUBLIC.value)
        )

        query = cls.filter_query(query, Workspace, filters)
        query = cls.search_query(query, Workspace, search)
        total_entries = query.count()
        query = cls.sort_query(query, Workspace, sort_field, sort_order)
        models_list = cls.paginate_query(query, page, per_page)
        total_pages = (total_entries + per_page - 1) // per_page

        user_namespace = UserValidationService.get_user_namespace(user_id)

        filtered_workspaces = []
        for workspace in models_list:
            raw_namespaces = workspace.namespaces
            if raw_namespaces == "*":
                filtered_workspaces.append(workspace)
            else:
                try:
                    namespaces = ast.literal_eval(raw_namespaces)
                    if user_namespace in namespaces:
                        filtered_workspaces.append(workspace)
                except:
                    continue

        return filtered_workspaces, total_entries, total_pages
