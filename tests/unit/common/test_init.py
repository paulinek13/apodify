from unittest.mock import patch, MagicMock
from apodify.common.init import init_apodify


@patch("apodify.common.init.Config")
@patch("apodify.common.init.logger")
def test_init_apodify(mock_logger, mock_config):
    mock_config._load_config = MagicMock()

    init_apodify()

    mock_logger.success.assert_called_once_with("Welcome to Apodify! Initializing...")
    mock_config._load_config.assert_called_once()
