from app.models.pg.user_profile import UserProfile


class UserValidationService:
    @staticmethod
    def get_user_namespace(user_id: int) -> str:
        user = UserProfile.get_by_id(user_id)
        return user.email.split("@")[1] if "@" in user.email else None
