
import pytest
from unittest.mock import patch, Mock
from distributions_extractor.clients.cms_medicare_utilization_client import CMSMedicareUtilizationClient 


@pytest.fixture
def client():
    return CMSMedicareUtilizationClient()


def test_get_utilization_success(client):
    mock_response = Mock()
    mock_response.json.return_value = {"npi": "1234567890", "year": "2022", "utilization": 100}
    mock_response.raise_for_status.return_value = None

    with patch.object(client.client, "get", return_value=mock_response) as mock_get:
        result = client.get_utilization("1234567890", year="2022")
        mock_get.assert_called_once_with(
            "https://data.cms.gov/data-api/v1/dataset/medicare-physician-utilization",
            params={"npi": "1234567890", "year": "2022"},
        )
        assert result == {"npi": "1234567890", "year": "2022", "utilization": 100}


def test_get_utilization_http_error(client):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch.object(client.client, "get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            client.get_utilization("1234567890", year="2022")
