import os

from apodify.common import path
from loguru import logger


def _validate_env_file() -> None:
    """
    Validate contents of the loaded .env file.
    """

    if os.environ.get("NASA_API_KEY") is None:
        logger.warning(
            "NASA_API_KEY is not set in the .env file. Demo key will be used."
        )
    elif not os.environ.get("NASA_API_KEY"):
        logger.warning("NASA_API_KEY is empty in the .env file. Demo key will be used.")
    elif os.environ.get("NASA_API_KEY") == "DEMO_KEY":
        logger.warning(
            "Using demo API key. Limited to 30 requests per hour. "
            "Consider setting your own API key in the .env file."
        )


def _load_env_file() -> None:
    """
    Load the environment variables from the .env file located in the home directory.
    """

    base_file_path = path.HOME_PATH / ".env"

    import dotenv

    if base_file_path.exists():
        dotenv.load_dotenv(base_file_path, override=True, interpolate=True)
        _validate_env_file()
    else:
        logger.warning(
            f"The .env file does not exist at {base_file_path}. Please create one to set your environment variables."
        )


def init_apodify() -> None:
    """
    Initialize Apodify. Must be called before using any other Apodify functionality.
    """

    logger.success("Welcome to Apodify! Initializing...")

    _load_env_file()
