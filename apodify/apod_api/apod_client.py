import requests

from datetime import datetime, date
from loguru import logger
from typing import Dict, Union

from apodify.common import Config
from apodify.internal import APODCache


class APODQueryBuilder:
    """
    Builder class for constructing APOD queries.

    This helper class simplifies building optimized queries for the APOD API.
    It supports fetching APODs for specific dates, date ranges, or random entries,
    and includes caching to reduce API calls and enhance performance.
    It is intended for use with the APODClient class.
    """

    def __init__(self, client):
        """
        Initialize the query builder.

        Args:
            client (APODClient): Reference to the parent client.
        """
        self._client = client

    def date(self, query_date: Union[str, date]) -> Dict:
        """
        Get APOD for a specific date.

        Args:
            query_date (Union[str, date]): Date of the APOD entry.

        Returns:
            Dictionary containing APOD details for the specified date.
        """
        return self._client._get_apod(query_date)

    def today(self) -> Dict:
        """
        Get APOD from today.

        Returns:
            Dictionary containing APOD details for today's date.
        """
        return self._client._get_apod(date.today())


class APODClient:
    """
    A client for interacting with [NASA's Astronomy Picture of the Day (APOD) API](https://api.nasa.gov/).
    """

    BASE_URL = "https://api.nasa.gov/planetary/apod"

    def __init__(self):
        """
        Initialize the APOD client.
        """
        self._cache = APODCache()
        self.api_key = Config.api_key

        self.get = APODQueryBuilder(self)

    def _validate_date(self, input_date: Union[str, date]) -> str:
        """
        Validate and convert input date to YYYY-MM-DD format.

        Args:
            input_date (Union[str, date]): Date in various formats.

        Returns:
            Formatted date string (YYYY-MM-DD).
        """
        if isinstance(input_date, date):
            return input_date.strftime("%Y-%m-%d")

        try:
            datetime.strptime(input_date, "%Y-%m-%d")  # try parsing string date
            return input_date
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD or date object.")

    def _get_apod(self, date: Union[str, date]) -> Dict:
        """
        Retrieve APOD data for a specific date.

        Args:
            date (Union[str, date]): Date of the APOD entry.

        Returns:
            Dictionary containing APOD details.
        """
        formatted_date = self._validate_date(date)

        if Config.use_cache:
            cached_data = self._cache.get_from_cache(formatted_date)
            if cached_data:
                logger.info(f"APOD for {formatted_date} retrieved from cache.")
                return cached_data
            else:
                logger.info(f"No cached APOD found for {formatted_date}.")

        params = {"api_key": self.api_key, "date": formatted_date}

        logger.info(f"Fetching APOD for {formatted_date} from NASA's APOD API...")

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        logger.info(
            f"Successfully fetched. Remaining requests: {response.headers.get('X-RateLimit-Remaining')}"
        )

        apod_data = response.json()
        logger.debug(apod_data)

        self._cache.save_to_cache(formatted_date, apod_data)

        return apod_data
