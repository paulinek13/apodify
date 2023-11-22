import apod
import colorama
import colors
import config
import datetime
import os
import traceback
import utils

from logger import logger


def main() -> None:
    apod_data = apod.get_apod_data()
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


if __name__ == "__main__":
    _start_time = datetime.datetime.now()

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

    logger.info(
        f"The program finished in {colorama.Style.BRIGHT}{(datetime.datetime.now() - _start_time).total_seconds()}{colorama.Style.NORMAL} sec!"
    )

    print()
