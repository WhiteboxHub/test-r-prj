import pytest
from unittest.mock import patch, MagicMock
from distributions_extractor.clients.hrsa_client import HRSAClient
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_client():
    """Fixture to patch httpx.Client"""
    with patch("distributions_extractor.clients.hrsa_client.httpx.Client") as MockHttpClient:
        mock_instance = MockHttpClient.return_value
        yield mock_instance

def test_get_state_workforce_success(mock_client):
    # Mock the JSON response
    mock_response = MagicMock()
    mock_response.json.return_value = [{"state": "NY", "year": "2022", "workforce_count": 1234}]
    mock_response.raise_for_status.return_value = None
    mock_client.get.return_value = mock_response

    client = HRSAClient()
    result = client.get_state_workforce("NY", "2022")

    # Check that httpx.Client.get was called with correct params
    mock_client.get.assert_called_once_with(
        "https://data.hrsa.gov/resource/ahrf.json",
        params={"state": "NY", "year": "2022"}
    )

    # Check the returned data
    assert result == [{"state": "NY", "year": "2022", "workforce_count": 1234}]

def test_get_state_workforce_http_error(mock_client):
    # Simulate an HTTP error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP error")
    mock_client.get.return_value = mock_response

    client = HRSAClient()

    with pytest.raises(Exception) as exc_info:
        client.get_state_workforce("CA", "2022")

    assert "HTTP error" in str(exc_info.value)