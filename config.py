import yaml

import utils


class get:
    """
    Default configuration settings.
    """

    # todo: add more info

    start_date = utils.TODAY
    end_date = utils.TODAY

    use_temp_apod_data = False
    use_hdurl = False

    save_url = True
    save_media_type = True
    save_content_type = False
    save_color_palette = True
    save_filterable_colors = True

    generate_combined_image = True

    extcolors_tolerance = 32
    extcolors_limit = 4


def init():
    """
    Load 'config.yml' file and update the configuration settings.
    """

    with open("config.yml", "r") as file:
        data = yaml.safe_load(file)
        # todo validate the input

        # todo: improve the code below

        if "start_date" in data:
            get.start_date = data["start_date"]
        if "end_date" in data:
            get.end_date = data["end_date"]

        if "use_temp_apod_data" in data:
            get.use_temp_apod_data = data["use_temp_apod_data"]
        if "use_hdurl" in data:
            get.use_hdurl = data["use_hdurl"]

        if "save_url" in data:
            get.save_url = data["save_url"]
        if "save_media_type" in data:
            get.save_media_type = data["save_media_type"]
        if "save_content_type" in data:
            get.save_content_type = data["save_content_type"]
        if "save_color_palette" in data:
            get.save_color_palette = data["save_color_palette"]
        if "save_filterable_colors" in data:
            get.save_filterable_colors = data["save_filterable_colors"]

        if "generate_combined_image" in data:
            get.generate_combined_image = data["generate_combined_image"]
        if "extcolors_tolerance" in data:
            get.extcolors_tolerance = data["extcolors_tolerance"]
        if "extcolors_limit" in data:
            get.extcolors_limit = data["extcolors_limit"]
