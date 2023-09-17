import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw

from logger import logger

load_dotenv()


def get_apod_data(start_date: str, end_date: str) -> List[Dict[str, Union[str, int]]]:
    """
    Retrieves Astronomy Picture of the Day (APOD) data for a specified date range.

    Args:
        start_date (str, optional): The start date for the APOD data range in the format "YYYY-MM-DD".
        end_date (str, optional): The end date for the APOD data range in the format "YYYY-MM-DD".

    Returns:
        list: A list of dictionaries, where each dictionary represents APOD data for a specific date.
    """

    # todo: start_date >= "1995-06-16" (the date when APOD started)
    # todo: end_date <= today

    logger.info(f"Retrieving APOD data ({start_date} - {end_date}) ...")

    base_url = "https://api.nasa.gov/planetary/apod"
    url = f"{base_url}?api_key={os.getenv('NASA_API_KEY')}&start_date={start_date}&end_date={end_date}"

    response = requests.get(url)

    if response.status_code == 200:
        logger.info("Request was successful (status code 200).")

        logger.debug(
            f"X-RateLimit-Remaining: {response.headers.get('X-RateLimit-Remaining')}."
        )

        apod_data = response.json()
        logger.debug(f"{len(apod_data)} day/s total.")

        # todo: add option to disable it
        logger.info("Writing response json to '/.temp/apod_data.json' ...")
        outfile = Path(f"./.temp/apod_data.json")
        outfile.parent.mkdir(exist_ok=True, parents=True)
        outfile.write_text(json.dumps(apod_data, indent=4))

        return apod_data
    else:
        raise Exception(
            {
                "message": "Failed to get data from APOD API",
                "status_code": response.status_code,
                "data": json.loads(response) if response else None,
            }
        )


def fetch_apod_image(url: str) -> Image.Image:
    """
    Fetches an APOD image from a given URL, saves it locally (./.temp/apod_image), and returns a Pillow's Image object.

    Args:
        url (str): The URL of the image to fetch.

    Returns:
        PIL.Image.Image: A Pillow's Image object representing the fetched image.
    """

    urllib.request.urlretrieve(url, "./.temp/apod_image")
    img = Image.open("./.temp/apod_image")
    return img


def save_apod_data(
    date: str, color_palette: List[str], filterable_colors: List[str], url: str
) -> None:
    """
    Saves APOD data (for a single day) to a JSON file.

    Args:
        date (str): The date for which the APOD data is saved (e.g., "2023-09-15").
        color_palette (List[str]): A color palette associated with the APOD.
        filterable_colors (List[str]): A filterable color palette based on the color palette.
        url (str): The URL of the APOD image on which the palettes are based.
    """

    dict_data = {
        "date": date,
        "colors": color_palette,
        "filterable": filterable_colors
        # "url": url,
    }
    final_data_json = json.dumps(dict_data, indent=4)
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    outfile = Path(
        f"./.output/data/{date_obj.year}/{str(date_obj.month).zfill(2)}/{str(date_obj.day).zfill(2)}.json"
    )
    outfile.parent.mkdir(exist_ok=True, parents=True)
    outfile.write_text(final_data_json)


def generate_combined_image(
    img: Image.Image, date: str, color_palette: List[str], filterable_colors: List[str]
) -> None:
    """
    Generates a combined image from an APOD image, its color palette, and filterable colors.

    Args:
        apod_image (PIL.Image.Image): The APOD image to include in the combined image.
        date (str): The APOD date for which the image is generated (YYYY-MM-DD).
        color_palette (List[str]): The color palette associated with the APOD image.
        filterable_colors (List[str]): The filterable colors corresponding to the color palette.
    """

    img_width, img_height = img.size
    new_image = Image.new(
        "RGB", (img_width + 10 + 100 + 10 + 100 + 10, img_height), "white"
    )
    new_image.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_image)

    rec_height = (img_height - 20) / len(color_palette)

    pos_x = img_width + 10
    pos_y = 10

    for i, color in enumerate(color_palette):
        draw.rectangle(
            [
                (pos_x, pos_y + i * rec_height),
                (pos_x + 100, pos_y + (i + 1) * rec_height),
            ],
            fill=color,
            outline=None,
        )

    pos_x = img_width + 10 + 100 + 10
    pos_y = 10

    for i, color in enumerate(filterable_colors):
        draw.rectangle(
            [
                (pos_x, pos_y + i * rec_height),
                (pos_x + 100, pos_y + (i + 1) * rec_height),
            ],
            fill=color,
            outline=None,
        )

    Path(f"./.output/images/{date}-2.jpg").parent.mkdir(exist_ok=True, parents=True)
    new_image.save(f"./.output/images/{date}-2.jpg", "JPEG")
