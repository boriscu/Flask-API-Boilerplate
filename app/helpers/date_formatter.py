from datetime import datetime


class DateFormatter:
    @staticmethod
    def date_from_string(date_str: str):
        """Convert a date string into a datetime.date object."""
        try:
            if date_str is not None:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            return None
        except ValueError:
            raise ValueError("This is not a valid date. Use YYYY-MM-DD format.")
