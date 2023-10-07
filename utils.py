from datetime import datetime


def is_date_within_range(date: str, start_date: str, end_date: str) -> bool:
    _date = datetime.strptime(date, "%Y-%m-%d")
    _start_date = datetime.strptime(start_date, "%Y-%m-%d")
    _end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return _start_date <= _date <= _end_date


TODAY: str = datetime.now().strftime("%Y-%m-%d")
