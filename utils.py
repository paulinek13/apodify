import json
from datetime import datetime

VERSION: str = "0.0.1"


class CriticalError(Exception):
    """Critical exception that prevents the program from working properly."""

    def __init__(self, message, json_data=None):
        if json_data is None:
            super().__init__(message)
        else:
            super().__init__(f"{message}\n{json.dumps(json_data, indent=4)}")


def is_date_within_range(date: str, start_date: str, end_date: str) -> bool:
    return (
        datetime.strptime(start_date, "%Y-%m-%d")
        <= datetime.strptime(date, "%Y-%m-%d")
        <= datetime.strptime(end_date, "%Y-%m-%d")
    )


TODAY: str = datetime.now().strftime("%Y-%m-%d")
