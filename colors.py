import colorsys
import math
from typing import List, Tuple

import extcolors
from PIL import Image, ImageDraw

import config
from logger import logger


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Converts an RGB color represented as a tuple, e.g.: (232, 166, 0), to its hexadecimal representation.

    Args:
        rgb (tuple): A tuple representing an RGB color, where rgb[0] is the red component, rgb[1] - green, and rgb[2] - blue.

    Returns:
        str: A string representing the hexadecimal color code in the format "#RRGGBB".
    """

    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Converts a hexadecimal color code to an RGB tuple.

    Args:
        hex_color (str): A hexadecimal color code (e.g., "#f325a9").

    Returns:
        Tuple[int, int, int]: An RGB tuple where each component (R, G, B) is an integer in the range [0, 255].
    """

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)


def _generate_filter_colors() -> List[Tuple[int, int, int]]:
    """
    Generates a list of visually distinct colors for filtering purposes.
    Also a preview image is generated.

    Returns:
        List[Tuple[int, int, int]]: A list of RGB tuples representing the generated colors.
    """

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
    return rgb_colors


def extract_colors(img: Image.Image) -> List[Tuple[int, int, int]]:
    """
    Extracts main/distinct/prominent colors (basically - a color palette) from an image and returns them as RGB tuples.

    Args:
        img: An image from which colors will be extracted. Should be a Pillow's Image object.

    Returns:
        List[Tuple[int, int, int]]: A list of extracted colors.

    Note:
        A lower 'tolerance' value results in more distinct colors being extracted.
        The `limit` parameter determines the maximum number of colors to be extracted from the image.
    """

    colors = extcolors.extract_from_image(
        img, config.get.extcolors_tolerance, config.get.extcolors_limit
    )
    return [(r, g, b) for (r, g, b), _ in colors[0]]


_FILTER_COLORS = None


def _find_closest_color(
    color: Tuple[int, int, int], palette: List[Tuple[int, int, int]]
) -> Tuple[int, int, int]:
    """
    Finds the closest color in a given palette to the specified color.

    Args:
        color (Tuple[int, int, int]): The RGB color for which to find the closest match.
        palette (List[Tuple[int, int, int]]): The palette of RGB colors to search within.

    Returns:
        Tuple[int, int, int]: The closest RGB color from the palette.

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

    return closest_color


def find_closest_colors(color_palette: List[Tuple[int, int, int]]) -> List[str]:
    """
    Finds the closest colors for each color in the given palette.

    Args:
        color_palette (List[Tuple[int, int, int]]): The palette of RGB colors.

    Returns:
        List[str]: A list of hexadecimal color codes representing the closest colors.
    """

    global _FILTER_COLORS
    if _FILTER_COLORS is None:
        _FILTER_COLORS = _generate_filter_colors()

    filterable_colors = []
    for color in color_palette:
        filterable_colors.append(rgb_to_hex(_find_closest_color(color, _FILTER_COLORS)))
    return filterable_colors
