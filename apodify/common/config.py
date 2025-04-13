from loguru import logger

from apodify.common import path


def _load_env_file() -> None:
    """
    Load environment variables from the .env file located in the home directory.

    This function uses the `dotenv` library to load the variables into the environment.
    """

    base_file_path = path.HOME_PATH / ".env"

    import dotenv

    if base_file_path.exists():
        dotenv.load_dotenv(base_file_path, override=True, interpolate=True)
    else:
        logger.warning(
            f"The .env file does not exist at {base_file_path}. Please create one to set your environment variables."
        )


def _should_use_demo_key() -> bool:
    """
    Determine whether to use the NASA demo API key or a custom key.

    Returns:
        bool: True if the demo key should be used, False if a custom key is available and valid.
    """
    import os

    key = os.environ.get("NASA_API_KEY", "").strip()

    if not key:
        logger.warning("NASA_API_KEY is not set or empty. Demo key will be used.")
        return True

    if key == "DEMO_KEY":
        logger.warning(
            "Using demo API key. Limited to 30 requests per hour."
            " Consider setting your own API key in the environment variables."
        )
        return True

    return False  # valid custom key available


class Config:
    """
    Configuration class for Apodify. Loads settings from the config file and environment variables.

    Access configuration options as class attributes.

    Example:
        >>> from apodify.common import Config
        >>> print(Config.log_level)
    """

    _is_loaded = False  # track if load_config has been called

    api_key = "DEMO_KEY"
    log_level = "INFO"

    def __new__(cls):
        # Prevent instantiation of the Config class
        raise TypeError("Config class cannot be instantiated.")

    @classmethod
    def _load_config(cls):
        """
        Load configuration from the config files: `config.toml` and `.env`.
        This method is called by `init_apodify` and should not be called directly.
        """
        if cls._is_loaded:
            logger.warning("Config has already been loaded. Skipping load.")
            return

        _load_env_file()

        if not _should_use_demo_key():
            import os

            cls.api_key = os.environ.get("NASA_API_KEY", "").strip()

        # TODO: load config from config.toml

        cls._is_loaded = True
