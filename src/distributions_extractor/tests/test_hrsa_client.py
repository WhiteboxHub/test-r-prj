import pytest
from unittest.mock import patch, MagicMock
from distributions_extractor.clients.hrsa_client import HRSAClient
from unittest.mock import patch, MagicMock
from distributions_extractor.clients.medscape_client import MedscapeClient


#This is test case for Hrsa client 
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






# This is Test case for medscapce

@pytest.fixture
def client():
    return MedscapeClient()


def test_get_compensation_survey_default(client):
    result = client.get_compensation_survey()
    assert result["specialty"] == "Pulmonology"
    assert result["avg_income"] == 310000
    assert result["gender_split"]["male"] == 0.70
    assert result["gender_split"]["female"] == 0.30
    assert sum(result["practice_setting"].values()) == pytest.approx(1.0)


def test_get_compensation_survey_custom_specialty(client):
    result = client.get_compensation_survey(specialty="Cardiology")
    assert result["specialty"] == "Cardiology"
    assert result["avg_income"] == 310000
