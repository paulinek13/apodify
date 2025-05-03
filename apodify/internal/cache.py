import json
import pathlib
from datetime import date, datetime
from typing import Dict, Optional, Union

from loguru import logger

from apodify.common import Config, path


class APODCache:
    """
    Manages the caching of APOD API responses.
    Each date has its own cache file in a directory structure: cache/YYYY/MM/DD
    """

    def __init__(self):
        """Initialize the cache manager."""
        self.enabled = Config.use_cache
        self.base_dir = path.CACHE_PATH

    def get_cache_path(self, request_date: Union[str, date]) -> pathlib.Path:
        """
        Get the path to the cache file for the specified date.

        Args:
            request_date (Union[str, date]): Date for the APOD entry.

        Returns:
            pathlib.Path: Path to the cache file.
        """
        if isinstance(request_date, str):
            date_obj = datetime.strptime(request_date, "%Y-%m-%d").date()
        else:
            date_obj = request_date

        cache_dir = (
            self.base_dir
            / str(date_obj.year)
            / f"{date_obj.month:02d}"
            / f"{date_obj.day:02d}"
        )
        return cache_dir / "apod.json"

    def get_from_cache(self, request_date: Union[str, date]) -> Optional[Dict]:
        """
        Retrieve APOD data from cache for the specified date if available.

        Args:
            request_date (Union[str, date]): Date for the APOD entry.

        Returns:
            Optional[Dict]: Cached APOD data or None if not in cache.
        """
        if not self.enabled:
            return None

        cache_path = self.get_cache_path(request_date)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r") as cache_file:
                cache_data = json.load(cache_file)
                return cache_data
        except Exception as e:
            logger.warning(f"Error reading cache for date {request_date}: {e}")
            return None

    def save_to_cache(self, request_date: Union[str, date], data: Dict) -> bool:
        """
        Save APOD data to cache for the specified date.

        Args:
            request_date (Union[str, date]): Date for the APOD entry.
            data (Dict): APOD data to cache.

        Returns:
            bool: True if saved successfully, False otherwise.
        """
        if not self.enabled:
            return False

        cache_path = self.get_cache_path(request_date)

        try:
            cache_path.parent.mkdir(parents=True, exist_ok=True)

            with open(cache_path, "w") as cache_file:
                json.dump(data, cache_file, indent=4)
                logger.debug(f"Saved data to cache for date: {request_date}")
                return True
        except Exception as e:
            logger.warning(f"Error writing to cache for date {request_date}: {e}")
            return False
