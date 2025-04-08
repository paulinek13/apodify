from apodify.common import path


def _load_env_file() -> None:
    """Load the environment variables from the .env file located in the home directory."""

    base_file_path = path.HOME_PATH / ".env"

    print("Loading environment variables from:", base_file_path)
    print("Base file path:", path.HOME_PATH)
    print("Apodify path:", path.APODIFY_PATH)

    # TODO: load the .env file

def init_apodify() -> None:
    """
    Initialize Apodify. Must be called before using any other Apodify functionality.
    """
    
    _load_env_file()
