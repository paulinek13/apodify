import config
from apod import *
from colors import extract_colors, find_closest_colors, rgb_to_hex
from logger import logger


def main():
    apod_data = get_apod_data(config.START_DATE, config.END_DATE)
    logger.info("Generating and categorizing color palettes for the data ...")
    # todo: progress bar

    for apod in apod_data:
        media_type = apod["media_type"]

        # todo: usage of thumbnails for video content to ensure that color data (color palette) is included in every APOD
        # fix: see apod data for 2010-07-25
        if media_type != "image":
            continue

        date = apod["date"]
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
    main()
# try:
# except Exception as e:
#     try:
#         logger.error(f"\n{json.dumps(e.args, indent=4)}")
#     except Exception as critical:
#         print(critical)
#         logger.critical(critical)
