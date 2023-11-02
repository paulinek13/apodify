import apod
import colors
import config
import os
import traceback
import utils

from logger import logger


def main():
    apod_data = apod.get_apod_data(config.get.start_date, config.get.end_date)
    logger.info("Generating and categorizing color palettes for the data ...")
    # todo: progress bar

    for apod_item in apod_data:
        media_type = apod_item["media_type"]

        # fix: see apod data for 2010-07-25
        if media_type not in ["image", "video"]:
            logger.critical("media type not recognized; skipping this day!")
            continue

        date = apod_item["date"]

        if media_type == "video":
            url = apod_item["thumbnail_url"]
        elif config.get.use_hdurl is True and apod_item["hdurl"] is not None:
            url = apod_item["hdurl"]
        else:
            url = apod_item["url"]

        img, content_type = apod.fetch_apod_image(url)
        color_palette = colors.extract_colors(img)
        filterable_colors = (
            colors.find_closest_colors(color_palette)
            if config.get.save_filterable_colors is True
            else None
        )

        hex_color_palette = []
        for color in color_palette:
            hex_color_palette.append(colors.rgb_to_hex(color))

        logger.debug(f"{date}")

        apod.save_apod_data(
            date, hex_color_palette, filterable_colors, url, media_type, content_type
        )
        apod.generate_combined_image(img, date, hex_color_palette, filterable_colors)

    # todo: "finished in": measure time (for individual images as well)
    logger.info("... finished!")


if __name__ == "__main__":
    try:
        config.init()

        os.makedirs("./.output/images/", exist_ok=True)
        os.makedirs("./.output/data/", exist_ok=True)
        os.makedirs("./.temp/", exist_ok=True)

        main()
    except utils.CriticalError as critical_error:
        logger.critical(critical_error)
    except Exception as exception:
        logger.critical(traceback.format_exc())
