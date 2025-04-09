import requests
from datetime import datetime, date
from loguru import logger
from typing import Dict, Union


class APODClient:
    """
    A client for interacting with [NASA's Astronomy Picture of the Day (APOD) API](https://api.nasa.gov/).
    """

    BASE_URL = "https://api.nasa.gov/planetary/apod"

    def __init__(self, api_key: str = "DEMO_KEY"):
        """
        Initialize the APOD client with a NASA API key.

        Args:
            api_key (str): NASA API key used for authentication.
        """
        self.api_key = api_key

    def _validate_date(self, input_date: Union[str, date]) -> str:
        """
        Validate and convert input date to YYYY-MM-DD format.

        Args:
            input_date (Union[str, date]): Date in various formats.

        Returns:
            Formatted date string (YYYY-MM-DD).
        """
        if isinstance(input_date, (date)):
            return input_date.strftime("%Y-%m-%d")

        try:
            datetime.strptime(input_date, "%Y-%m-%d")  # try parsing string date
            return input_date
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD or date object.")

    def get_apod(self, date: Union[str, date]) -> Dict:
        """
        Retrieve APOD data for a specific date.

        Args:
            date (Union[str, date]): Date of the APOD entry.

        Returns:
            Dictionary containing APOD details.
        """
        formatted_date = self._validate_date(date)
        params = {"api_key": self.api_key, "date": formatted_date}

        if self.api_key == "DEMO_KEY":
            logger.warning("Using demo API key. Limited to 30 requests per hour.")

        logger.info(f"Retrieving APOD for date: {formatted_date} ...")

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        logger.debug(response.json())

        logger.info(
            f"Remaining requests: {response.headers.get('X-RateLimit-Remaining')} (X-Ratelimit-Limit: {response.headers.get('X-RateLimit-Limit')})"
        )

        return response.json()
