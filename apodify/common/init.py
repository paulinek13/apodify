from loguru import logger

from apodify.common.config import Config


def init_apodify() -> None:
    """
    Initialize Apodify. Must be called before using any other Apodify functionality.
    """

    logger.success("Welcome to Apodify! Initializing...")

    Config._load_config()
