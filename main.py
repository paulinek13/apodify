import apod
import colors
import config
import os
import traceback
import utils

from logger import logger


def main():
    apod_data = apod.get_apod_data(config.get.start_date, config.get.end_date)
    # todo: progress bar

    for apod_item in apod_data:
        print()

        apod.extend_apod(
            apod_item["date"],
            apod_item["title"],
            apod_item["url"],
            apod_item["hdurl"] if "hdurl" in apod_item else None,
            apod_item["thumbnail_url"] if "thumbnail_url" in apod_item else None,
            apod_item["media_type"],
            apod_item["explanation"],
        )

    print()

    # todo: "finished in": measure time (for individual images as well)
    logger.info("... finished!")


if __name__ == "__main__":
    try:
        utils.print_start_info()
        config.init()

        os.makedirs("./.output/images/", exist_ok=True)
        os.makedirs("./.output/data/", exist_ok=True)
        os.makedirs("./.temp/", exist_ok=True)

        colors.generate_filter_colors()

        main()
    except utils.CriticalError as critical_error:
        logger.critical(critical_error)
    except Exception as exception:
        logger.critical(traceback.format_exc())

    print()
