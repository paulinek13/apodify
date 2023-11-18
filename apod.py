import colorama
import colors
import config
import datetime
import dotenv
import json
import os
import pathlib
import requests
import typing
import utils

from PIL import Image, ImageDraw
from logger import logger

dotenv.load_dotenv()


def get_apod_data() -> typing.List[typing.Dict[str, typing.Union[str, int]]]:
    """Retrieve Astronomy Picture of the Day (APOD) data for a specified date range.

    Returns:
        A list of dictionaries, where each dictionary represents APOD data for a specific date.
    """

    if config.get.use_temp_apod_data:
        if os.path.isfile(".temp/apod_data.json") is True:
            with open(".temp/apod_data.json", encoding="utf-8") as file:
                data = json.loads(file.read())
                logger.info("APOD data loaded from the temporary file.")
                return data
        else:
            logger.warning("The temp file with APOD items was not found!")

    if not utils.is_date_within_range(config.get.start_date, "1995-06-16", utils.TODAY):
        raise utils.CriticalError(
            "'START_DATE' cannot be later than the present day or earlier than '1995-06-16' (the day APOD started)"
        )

    if not utils.is_date_within_range(config.get.end_date, "1995-06-16", utils.TODAY):
        raise utils.CriticalError(
            "'END_DATE' cannot be later than the present day or earlier than '1995-06-16' (the day APOD started)"
        )

    logger.info(
        f"Retrieving APOD data ({f'{config.get.start_date} - {config.get.end_date}' if config.get.date is None else f'{config.get.date}'}) ..."
    )

    base_url = "https://api.nasa.gov/planetary/apod"

    # using the search parameters 'start_date' and 'end_date' even for a single day
    # instead of just 'date', because the APOD API returns the data as a table in such cases;
    query = (
        f"start_date={config.get.start_date}&end_date={config.get.end_date}"
        if config.get.date is None
        else f"start_date={config.get.date}&end_date={config.get.date}"
    )

    url = f"{base_url}?api_key={os.getenv('NASA_API_KEY')}&{query}&thumbs=true"

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
        pathlib.Path(f"./.temp/apod_data.json").write_text(
            json.dumps(apod_data, indent=4)
        )

        return apod_data
    else:
        raise utils.CriticalError(
            "Failed to get data from APOD API",
            {
                "url": response.url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "response": response.json(),
            },
        )


def fetch_apod_image(url: str) -> tuple[Image.Image, str, tuple[int, int]]:
    """Fetch an APOD image from a given URL and save it locally.

    Args:
        url: The URL of the image to fetch.

    Returns:
        A tuple containing two elements:
            - A Pillow's Image object representing the fetched image.
            - A string representing the content type of the fetched image.
            - A tuple containing the size of the image (width, height).

    Notes:
        The retrieved image is saved at ./.temp/apod_image.
    """

    logger.info(f"Fetching an APOD image ...")

    response = requests.get(url)

    if response.status_code == 200:
        content_type = response.headers.get("content-type")

        if content_type and content_type.startswith("image/"):
            img_data = response.content
            with open("./.temp/apod_image", "wb") as handler:
                handler.write(img_data)
            img = Image.open("./.temp/apod_image")
            return img, content_type, img.size
        else:
            # todo: extract colors from a link/page anyway?
            logger.warning("The URL does not point to an image.", {"url": url})
            return None, content_type
    elif response.status_code == 406:
        logger.warning(
            f"406 Not Acceptable, see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406"
        )

    return None, response.headers.get("content-type")


def save_apod_data(
    date: str,
    color_palette: typing.List[str],
    filterable_colors: typing.List[str],
    url: str,
    media_type: str,
    content_type: str,
    img_size: tuple[int, int],
) -> None:
    """Save APOD data (for a single day) to a JSON file.

    Args:
        date: The date for which the APOD data is saved (format: "YYYY-MM-DD").
        color_palette: The color palette associated with the APOD.
        filterable_colors: The filterable color palette based on the color palette.
        url: The URL of the APOD image on which the palettes are based.
        media_type: The media type returned by the APOD API.
        content_type: The content type of the image.
        img_size: the size of the image (width, height).
    """

    logger.info(f"Saving APOD data ...")

    dict_data = {
        "date": date,
    }

    if config.get.save_url is True:
        dict_data["url"] = url
    if config.get.save_media_type is True:
        dict_data["media_type"] = media_type
    if config.get.save_content_type is True:
        dict_data["content_type"] = content_type
    if config.get.save_color_palette is True:
        dict_data["colors"] = color_palette
    if config.get.save_filterable_colors is True:
        dict_data["filterable"] = filterable_colors
    if config.get.save_img_width is True:
        dict_data["width"] = img_size[0]
    if config.get.save_img_height is True:
        dict_data["height"] = img_size[1]
    if config.get.save_img_wh_ratio:
        dict_data["wh_ratio"] = round(img_size[0] / img_size[1], 2)

    final_data_json = json.dumps(dict_data, indent=4)
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    outfile = pathlib.Path(
        f"./.output/data/{date_obj.year}/{str(date_obj.month).zfill(2)}/{str(date_obj.day).zfill(2)}.json"
    )
    outfile.parent.mkdir(exist_ok=True, parents=True)
    outfile.write_text(final_data_json)


def generate_combined_image(
    img: Image.Image,
    date: str,
    color_palette: typing.List[str],
    filterable_colors: typing.List[str],
) -> None:
    """Generate a combined image from an APOD image, its color palette, and filterable colors.

    Args:
        apod_image: The APOD image to be included in the combined image. Must be a Pillow's Image object.
        date: The APOD date for which the image is generated (YYYY-MM-DD).
        color_palette: The color palette associated with the APOD image.
        filterable_colors: The filterable colors corresponding to the color palette.
    """

    if config.get.generate_combined_image is False:
        return

    logger.info(f"Generating a combined image for previewing results ...")

    # todo: improve this implementation

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

    if config.get.save_filterable_colors is True:
        for i, color in enumerate(filterable_colors):
            draw.rectangle(
                [
                    (pos_x, pos_y + i * rec_height),
                    (pos_x + 100, pos_y + (i + 1) * rec_height),
                ],
                fill=color,
                outline=None,
            )

    new_image.save(f"./.output/images/{date}.jpg", "JPEG")


def extend_apod(
    date: str,
    title: str,
    url: str,
    hdurl: str | None,
    thumbnail_url: str | None,
    media_type: str,
    explanation: str,
) -> bool:
    """Extend an APOD day with additional properties.

    Args:
        date: Date of an APOD.
        title: The title of the APOD.
        url: The URL of the APOD image or thumbnail of the APOD video. Used for color extraction.
        hdurl: The URL for any high-resolution image for that day.
        thumbnail_url: The URL of thumbnail of the video.
        media_type: May be 'image' or 'video', based on content. # fix: see apod data for 2010-07-25
        explanation: The text explanation of the APOD.

    Returns:
        A boolean: True is the operation was succesfull and False in case of an error.

    """

    _apod_start_time = datetime.datetime.now()

    print(colorama.Fore.YELLOW + f"{' ' * 20} {date}")

    # todo: validate the input, in case of an error throw an exception OR just skip the APOD/day (configurable)
    # todo: check if a date is within range specified in the config file

    if media_type not in ["image", "video"]:
        logger.critical("The media type was not recognized!")
        logger.warning("Skipping this day!")
        return False

    _img_url = ""

    if media_type == "video" and thumbnail_url:
        _img_url = thumbnail_url
    elif config.get.use_hdurl is True and hdurl:
        _img_url = hdurl
    else:
        # fix: make sure it points to an image url
        _img_url = url

    logger.info(f"Extending APOD from {date} ...")

    logger.debug(f"                 {date} / {title} / {media_type}")
    logger.debug(f"url:             {url}")
    logger.debug(f"hdurl:           {hdurl}")
    if thumbnail_url is not None:
        logger.debug(f"thumbnail_url:   {thumbnail_url}")
    # logger.debug(f"explanation:     {explanation}")
    logger.debug(f"_img_url:        {_img_url}")

    _img, _content_type, _img_size = fetch_apod_image(_img_url)

    _filterable_colors = []
    _hex_colors_palette = []

    if _img is not None:
        _colors_palette = colors.extract_colors(_img)
        _filterable_colors = (
            colors.find_closest_colors(_colors_palette)
            if config.get.save_filterable_colors is True
            else None
        )

        _hex_colors_palette = []
        for _color in _colors_palette:
            _hex_colors_palette.append(colors.rgb_to_hex(_color))

    save_apod_data(
        date,
        _hex_colors_palette,
        _filterable_colors,
        _img_url,
        media_type,
        _content_type,
        _img_size,
    )

    if _img is not None:
        generate_combined_image(_img, date, _hex_colors_palette, _filterable_colors)

    logger.info(
        f"Finished in {colorama.Style.BRIGHT}{(datetime.datetime.now() - _apod_start_time).total_seconds()}{colorama.Style.NORMAL} sec!"
    )

    return True
