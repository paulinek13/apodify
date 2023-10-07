import json


class CriticalError(Exception):
    """Critical exception that prevents the program from working properly."""

    def __init__(self, message, json_data=None):
        if json_data is None:
            super().__init__(message)
        else:
            super().__init__(f"{message}\n{json.dumps(json_data, indent=4)}")
