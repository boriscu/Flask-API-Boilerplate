from typing import Callable
from flask import request


class PreRequestManager:
    """Manage pre-request operations across various endpoints.

    This class provides a static method to apply a specific function to requests that match certain criteria.
    """

    @staticmethod
    def pre_request_handler(
        base_path: str, pre_request_function: Callable, exclusions: list[str] = []
    ):
        """Execute a function before requests to specified paths, excluding certain paths.

        Args:
            base_path (str): The base path of the endpoints to apply the function.
            pre_request_function (Callable): The function to execute for matching requests.
            exclusions (List[str]): Paths to exclude from the pre-request checks.
        """

        full_exclusions = [base_path + exc for exc in exclusions]

        if request.path.startswith(base_path) and not any(
            request.path.startswith(exc) for exc in full_exclusions
        ):
            pre_request_function()
