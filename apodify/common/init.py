from apodify.common import path
from loguru import logger


def _load_env_file() -> None:
    """Load the environment variables from the .env file located in the home directory."""

    base_file_path = path.HOME_PATH / ".env"

    import dotenv

    if base_file_path.exists():
        dotenv.load_dotenv(base_file_path, override=True, interpolate=True)
        logger.success("Loaded environment variables from the .env file")
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
