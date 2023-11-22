import colorsys
import config
import extcolors
import math
import typing

from PIL import Image, ImageDraw
from logger import logger

_FILTER_COLORS = None


def rgb_to_hex(rgb: typing.Tuple[int, int, int]) -> str:
    """Convert an RGB color represented as a tuple to its hexadecimal representation."""
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex_color: str) -> typing.Tuple[int, int, int]:
    """Convert a hexadecimal color code to an RGB tuple."""

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)


def generate_filter_colors() -> None:
    """Generate a list of visually distinct colors for filtering purposes.

    A preview image of the colors is generated as well.
    """

    global _FILTER_COLORS
    if _FILTER_COLORS is not None:
        return

    logger.info(
        "Generating a list of filterable colors and a preview image for them ..."
    )

    img_width = 16 * 10
    img_height = 12 * 10
    image = Image.new("RGBA", (img_width + 20, img_height + 10))
    draw = ImageDraw.Draw(image)

    rec_pos_y = 0

    hex_colors = []

    for x in range(12):
        rec_pos_x = 0
        draw.rectangle([0, rec_pos_y, 10, rec_pos_y + 10], fill="#000000")
        rec_pos_x += 10

        for xx in range(4):
            for xxx in range(4):
                h = 360 - (30 * x)
                s = 100 - (25 * xx)
                v = 100 - (25 * xxx)

                s = s / 100.0
                v = v / 100.0

                r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)

                hex_color = "#{:02X}{:02X}{:02X}".format(
                    int(r * (256 if r < 1 else 255)),
                    int(g * (256 if g < 1 else 255)),
                    int(b * (256 if b < 1 else 255)),
                )
                hex_colors.append(hex_color)

                draw.rectangle(
                    [rec_pos_x, rec_pos_y, rec_pos_x + 10, rec_pos_y + 10],
                    fill=hex_color,
                )
                rec_pos_x += 10

            draw.rectangle(
                [rec_pos_x, rec_pos_y, img_width + 20, rec_pos_y + 10], fill="#ffffff"
            )

        rec_pos_y += 10

    hex_colors.append("#000000")
    hex_colors.append("#333333")
    hex_colors.append("#666666")
    hex_colors.append("#999999")
    hex_colors.append("#cccccc")
    hex_colors.append("#ffffff")

    draw.rectangle([0, img_height, img_width + 10, img_height + 10], fill="#000000")

    draw.rectangle([10, img_height, 50, img_height + 10], fill="#333333")
    draw.rectangle([50, img_height, 90, img_height + 10], fill="#666666")
    draw.rectangle([90, img_height, 130, img_height + 10], fill="#999999")
    draw.rectangle([130, img_height, 170, img_height + 10], fill="#cccccc")

    draw.rectangle(
        [img_width + 10, img_height, img_width + 20, img_height + 10],
        fill="#ffffff",
    )

    image.save("./.output/filter_colors_preview.png")

    rgb_colors = [hex_to_rgb(hex_color) for hex_color in hex_colors]

    _FILTER_COLORS = rgb_colors


def extract_colors(img: Image.Image) -> typing.List[typing.Tuple[int, int, int]]:
    """Extract main/distinct/prominent colors (a color palette) from an image.

    Args:
        img: An image from which colors will be extracted. Must be a Pillow's Image object.

    Returns:
        A list of the extracted colors. Each color is represented as an RGB tuple.

    Notes:
        A lower 'tolerance' value results in more distinct colors being extracted.
        The `limit` parameter determines the maximum number of colors to be extracted from the image.
    """

    logger.info(f"Extracting colors from the image ...")

    colors = extcolors.extract_from_image(
        img, config.get.extcolors_tolerance, config.get.extcolors_limit
    )
    return [(r, g, b) for (r, g, b), _ in colors[0]]


def _find_closest_color(
    color: typing.Tuple[int, int, int],
    palette: typing.List[typing.Tuple[int, int, int]],
) -> typing.Tuple[int, int, int]:
    """Find the closest color in a given palette to a specified color.

    Args:
        color: The RGB color for which to find the closest match.
        palette: The palette of RGB colors to search within.

    Returns:
        The closest color from the palette represented as an RGB tuple.

    Note:
        This function calculates the closest color using Euclidean distance in the RGB color space.
    """

    closest_color = None
    min_distance = float("inf")

    for palette_color in palette:
        distance = math.sqrt(
            (color[0] - palette_color[0]) ** 2
            + (color[1] - palette_color[1]) ** 2
            + (color[2] - palette_color[2]) ** 2
        )

        if distance < min_distance:
            min_distance = distance
            closest_color = palette_color

    logger.debug(f"The closest color for {color}: {closest_color}")

    return closest_color


def find_closest_colors(
    color_palette: typing.List[typing.Tuple[int, int, int]]
) -> typing.List[str]:
    """Find the closest colors for each color in a given palette.

    Args:
        color_palette: The palette of RGB colors.

    Returns:
        A list of hexadecimal color codes representing the closest colors.
    """

    logger.info(f"Finding the closest colors ...")

    logger.debug(f"Color palette: {color_palette}")

    filterable_colors = []
    for color in color_palette:
        filterable_colors.append(rgb_to_hex(_find_closest_color(color, _FILTER_COLORS)))

    logger.debug(f"Filterable colors: {filterable_colors}")

    return filterable_colors
