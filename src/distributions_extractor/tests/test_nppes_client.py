import pytest
from unittest.mock import patch, Mock
from distributions_extractor.clients.nppes_client import NPPESClient  


@pytest.fixture
def client():
    return NPPESClient()


def test_search_providers_success(client):
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [{"number": 1, "name": "Dr. John Doe"}]
    }
    mock_response.raise_for_status.return_value = None

    with patch.object(client.client, "get", return_value=mock_response) as mock_get:
        result = client.search_providers(taxonomy="207RP1001X", state="CA", city="Los Angeles", limit=10)
        
        mock_get.assert_called_once_with(
            "https://npiregistry.cms.hhs.gov/api/",
            params={"version": "2.1", "taxonomy": "207RP1001X", "limit": 10, "state": "CA", "city": "Los Angeles"},
        )
        assert result == {"results": [{"number": 1, "name": "Dr. John Doe"}]}


def test_search_providers_http_error(client):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch.object(client.client, "get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            client.search_providers(taxonomy="207RP1001X")
