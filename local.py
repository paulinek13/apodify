import colorama
import datetime
import dotenv
import json
import os
import pathlib
import requests

from logger import logger

dotenv.load_dotenv()


def save_apods(start_date, end_date):
    """Save APOD data locally for a specific date range.

    Data from one APOD day corresponds to one file stored at `/.local_apod/data/{YYYY}/{MM}/{DD}.json`.
    """

    logger.info(f"Fetching APOD data for {start_date} - {end_date} ...")

    base_url = "https://api.nasa.gov/planetary/apod"
    query = f"start_date={start_date}&end_date={end_date}"
    url = f"{base_url}?api_key={os.getenv('NASA_API_KEY')}&{query}&thumbs=true"

    response = requests.get(url)

    if response.status_code == 200:
        logger.info("Request was successful (status code 200).")
        logger.debug(
            f"X-RateLimit-Remaining: {response.headers.get('X-RateLimit-Remaining')}."
        )

        apod_data = response.json()
        logger.info(f"{len(apod_data)} day/s total.")

        for apod in apod_data:
            date = apod["date"]

            logger.info(
                f"Saving APOD data from {colorama.Style.BRIGHT}{date}{colorama.Style.NORMAL} to a file ..."
            )

            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            outfile = pathlib.Path(
                f"./.local_apod/data/{date_obj.year}/{str(date_obj.month).zfill(2)}/{str(date_obj.day).zfill(2)}.json"
            )
            outfile.parent.mkdir(exist_ok=True, parents=True)
            outfile.write_text(json.dumps(apod, indent=4))

    else:
        return


def fetch_apods_by_year(year):
    if year == 1995:
        save_apods("1995-06-16", "1995-12-31")
    elif year == datetime.date.today().year:
        save_apods(f"{year}-01-01", f"{datetime.date.today()}")
    else:
        save_apods(f"{year}-01-01", f"{year}-12-31")


if __name__ == "__main__":
    for year in range(1995, 2024):
        fetch_apods_by_year(year)
