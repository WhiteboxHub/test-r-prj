
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





import pytest
import httpx
from unittest.mock import patch, MagicMock
from distributions_extractor.clients.cms_physician_compare_client import CMSPhysicianCompareClient 

@pytest.fixture
def client():
    return CMSPhysicianCompareClient()

def test_search_providers_success(client):
    fake_response_data = {
        "results": [
            {"name": "Dr. John Doe", "specialty": "Pulmonary Disease", "state": "CA"},
            {"name": "Dr. Jane Smith", "specialty": "Pulmonary Disease", "state": "NY"},
        ]
    }

    with patch.object(httpx.Client, "get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = fake_response_data
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = client.search_providers(specialty="Pulmonary Disease", state="CA", limit=2)

        mock_get.assert_called_once()
        assert isinstance(result, dict)
        assert "results" in result
        assert result["results"][0]["name"] == "Dr. John Doe"

def test_search_providers_with_state(client):
    with patch.object(httpx.Client, "get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"results": []}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        result = client.search_providers(specialty="Cardiology", state="TX", limit=1)

        
        args, kwargs = mock_get.call_args
        assert "state" in kwargs["params"]
        assert kwargs["params"]["state"] == "TX"
        assert result == {"results": []}

def test_search_providers_http_error(client):
    with patch.object(httpx.Client, "get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock()
        )
        mock_get.return_value = mock_resp

        with pytest.raises(httpx.HTTPStatusError):
            client.search_providers("Pulmonary Disease")