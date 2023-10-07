import json
from datetime import datetime


class CriticalError(Exception):
    """Critical exception that prevents the program from working properly."""

    def __init__(self, message, json_data=None):
        if json_data is None:
            super().__init__(message)
        else:
            super().__init__(f"{message}\n{json.dumps(json_data, indent=4)}")


def is_date_within_range(date: str, start_date: str, end_date: str) -> bool:
    _date = datetime.strptime(date, "%Y-%m-%d")
    _start_date = datetime.strptime(start_date, "%Y-%m-%d")
    _end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return _start_date <= _date <= _end_date


TODAY: str = datetime.now().strftime("%Y-%m-%d")
