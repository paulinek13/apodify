import pytest
from datetime import date
from unittest.mock import Mock, patch

from apodify.apod_api import APODClient


@pytest.fixture
def api_client():
    return APODClient()


def test_validate_date(api_client):
    """Test the date validation method"""

    string_value = "2025-01-01"
    assert api_client._validate_date(string_value) == string_value

    date_object = date(2024, 12, 31)
    assert api_client._validate_date(date_object) == "2024-12-31"

    with pytest.raises(ValueError):
        api_client._validate_date("invalid-date")


@patch("requests.get")
@patch("apodify.common.Config.use_cache", False)
def test_get_apod(mock_requests_get, api_client):
    """Test retrieving APOD for a specific date"""

    mock_response = Mock()
    mock_response.json.return_value = {
        "date": "2000-01-01",
        "title": "Test APOD",
        "url": "https://example.com/apod.jpg",
    }
    mock_response.raise_for_status = Mock()
    mock_requests_get.return_value = mock_response

    result = api_client.get.date("2000-01-01")

    mock_requests_get.assert_called_once_with(
        APODClient.BASE_URL, params={"api_key": "DEMO_KEY", "date": "2000-01-01"}
    )

    assert result["date"] == "2000-01-01"
    assert result["title"] == "Test APOD"
