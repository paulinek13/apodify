import pytest
import os
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from apodify.common.config import Config, _should_use_demo_key, _load_env_file


def test_config_cannot_be_instantiated():
    """Test that Config class cannot be instantiated"""
    with pytest.raises(TypeError, match="Config class cannot be instantiated"):
        Config()


@patch("apodify.common.config._load_env_file")
@patch("apodify.common.config._should_use_demo_key")
@patch("apodify.common.path.HOME_PATH")
def test_load_config_already_loaded(
    mock_home_path, mock_should_use_demo, mock_load_env
):
    """Test that _load_config doesn't reload if already loaded"""

    Config._is_loaded = True
    Config._load_config()

    mock_load_env.assert_not_called()
    mock_should_use_demo.assert_not_called()


@patch("apodify.common.config._load_env_file")
@patch("apodify.common.config._should_use_demo_key", return_value=True)
@patch("apodify.common.path.HOME_PATH")
def test_load_config_with_missing_settings(
    mock_home_path, mock_should_use_demo, mock_load_env
):
    """Test loading config with missing settings in toml file"""

    mock_config_path = MagicMock()
    mock_config_path.exists.return_value = True

    Config._is_loaded = False
    Config.debug = True
    Config.use_cache = True

    # Call the function with mocked file open and empty config
    with patch("builtins.open", mock_open(read_data=b"")):
        with patch("tomllib.load", return_value={}):
            Config._load_config()

    assert Config.debug is True
    assert Config.use_cache is True
    assert Config._is_loaded is True


@pytest.mark.parametrize(
    "api_key, expected_result",
    [("", True), ("DEMO_KEY", True), ("CUSTOM_API_KEY", False)],
)
@patch.dict(os.environ, {})
def test_should_use_demo_key(api_key, expected_result):
    """Test that _should_use_demo_key returns the correct value for different API keys"""
    with patch.dict(os.environ, {"NASA_API_KEY": api_key}):
        assert _should_use_demo_key() is expected_result


@patch("pathlib.Path.exists", return_value=False)
@patch("apodify.common.path.HOME_PATH", Path("/mock_home"))
def test_load_env_file_not_exists(mock_exists):
    """Test _load_env_file when .env file doesn't exist"""
    with patch("loguru.logger.warning") as mock_warning:
        _load_env_file()
        mock_warning.assert_called_once()


@patch("pathlib.Path.exists", return_value=True)
@patch("dotenv.load_dotenv")
@patch("apodify.common.path.HOME_PATH", Path("/mock_home"))
def test_load_env_file_exists(mock_load_dotenv, mock_exists):
    """Test _load_env_file when .env file exists"""
    _load_env_file()
    mock_load_dotenv.assert_called_once()
