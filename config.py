import yaml

import utils


class get:
    """
    Default configuration settings.
    """

    # todo: add more info

    start_date = utils.TODAY
    end_date = utils.TODAY

    save_url = True
    save_media_type = True
    save_color_palette = True
    save_filterable_colors = True

    generate_combined_image = True


def init():
    """
    Load 'config.yml' file and update the configuration settings.
    """
    with open("config.yml", "r") as file:
        data = yaml.safe_load(file)
        # todo validate the input

        get.start_date = data["start_date"]
        get.end_date = data["end_date"]

        get.save_url = data["save_url"]
        get.save_media_type = data["save_media_type"]
        get.save_color_palette = data["save_color_palette"]
        get.save_filterable_colors = data["save_filterable_colors"]
