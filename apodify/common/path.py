import pathlib

APODIFY_PATH = pathlib.Path(__file__, "..", "..").resolve()
HOME_PATH = pathlib.Path(APODIFY_PATH, "..").resolve()

CONFIG_PATH = pathlib.Path(APODIFY_PATH, "config.toml").resolve()
CACHE_PATH = pathlib.Path(HOME_PATH, "cache").resolve()
CACHE_PATH.mkdir(parents=True, exist_ok=True)
