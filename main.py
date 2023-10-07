import os
import traceback

import config
from apod import *
from colors import extract_colors, find_closest_colors, rgb_to_hex
from logger import logger
from utils import CriticalError


def main():
    apod_data = get_apod_data(config.get.start_date, config.get.end_date)
    logger.info("Generating and categorizing color palettes for the data ...")
    # todo: progress bar

    for apod in apod_data:
        media_type = apod["media_type"]

        # fix: see apod data for 2010-07-25
        if media_type not in ["image", "video"]:
            logger.critical("media type not recognized; skipping this day!")
            continue

        date = apod["date"]

        if media_type == "video":
            url = apod["thumbnail_url"]
        else:
            url = apod["url"]
        # hdurl = apod["hdurl"]  # todo

        img = fetch_apod_image(url)
        color_palette = extract_colors(img)
        filterable_colors = find_closest_colors(color_palette)

        hex_color_palette = []
        for color in color_palette:
            hex_color_palette.append(rgb_to_hex(color))

        logger.debug(f"{date}")

        save_apod_data(date, hex_color_palette, filterable_colors, url)
        generate_combined_image(img, date, hex_color_palette, filterable_colors)

    # todo: "finished in": measure time (for individual images as well)
    logger.info("... finished!")


if __name__ == "__main__":
    try:
        config.init()

        os.makedirs("./.output/images/", exist_ok=True)
        os.makedirs("./.output/data/", exist_ok=True)
        os.makedirs("./.temp/", exist_ok=True)

        main()
    except CriticalError as critical_error:
        logger.critical(critical_error)
    except Exception as exception:
        logger.critical(traceback.format_exc())
