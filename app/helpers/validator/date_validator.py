from datetime import datetime, _Date
from .validator import Validator


class DateValidator(Validator):
    def validate(self, date_str: str) -> _Date:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("This is not a valid date. Use YYYY-MM-DD format.")
