from typing import Any, Dict, List, Tuple

from app.models.pg.workspace import Workspace

from app.helpers.image_processor import ImageProcessor

from app.services.base_crud_services.base_pagination_service import (
    BasePaginationService,
)


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
        workspaces, total_entries, total_pages = super().get_rows(
            Workspace, page, per_page, sort_field, sort_order, search, filters
        )
        for workspace in workspaces:
            if workspace.icon_image:
                workspace.icon_image = ImageProcessor.encode_image(workspace.icon_image)

        return (workspaces, total_entries, total_pages)
