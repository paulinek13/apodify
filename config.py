import yaml

import utils


class get:
    start_date = utils.TODAY
    end_date = utils.TODAY


def init():
    with open("config.yml", "r") as file:
        data = yaml.safe_load(file)

        get.start_date = data["start_date"]
        get.end_date = data["end_date"]
