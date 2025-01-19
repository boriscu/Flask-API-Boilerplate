from app.endpoints.workspace_endpoints import workspace_pre_request


class PreRequestRegistrer:
    """Manage the registration of pre-request handlers for an application.

    Attributes:
        app (Flask): The Flask application to which pre-request handlers are attached.

    """

    def __init__(self, app):
        self.app = app

    def register_all(self):
        """Register all pre-request handlers."""

        self._register_workspace_checks()

    def _register_workspace_checks(self):
        """Register pre-request checks specific to workspace endpoints."""

        self.app.before_request(workspace_pre_request)
