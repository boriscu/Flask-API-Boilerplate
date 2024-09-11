from typing import Any, Dict, List, Tuple
from app.models.user_profile import UserProfile
from app.services.base_crud_services.base_pagination_service import (
    BasePaginationService,
)


class UserPaginationService(BasePaginationService):
    @classmethod
    def get_rows(
        cls,
        page: int,
        per_page: int,
        sort_field: str,
        sort_order: str,
        search: str,
        filters: Dict[str, Any],
    ) -> Tuple[List[UserProfile], int, int]:
        return super().get_rows(
            UserProfile, page, per_page, sort_field, sort_order, search, filters
        )
