import colorama
import json
import re

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


def is_valid_date_format(date_string: str) -> bool:
    return (
        True
        if re.match(
            # https://www.regular-expressions.info/dates.html
            r"^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$",
            date_string,
        )
        else False
    )


def print_start_info() -> None:
    print(colorama.Fore.YELLOW + "▁" * 32)
    print(colorama.Fore.YELLOW + "███ apod-extended " + "█" * 14)
    print(colorama.Fore.YELLOW + "▔" * 32)
    print(colorama.Style.RESET_ALL)
    pass


TODAY: str = datetime.now().strftime("%Y-%m-%d")
