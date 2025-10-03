import pytest
from unittest.mock import MagicMock
from distributions_extractor.distributions.pulmonologist_distribution_builder import PulmonologistDistributionBuilder
from requests import HTTPError

@pytest.fixture
def mock_clients():
    nppes = MagicMock()
    cms = MagicMock()
    hrsa = MagicMock()
    medscape = MagicMock()


    nppes.search_providers.return_value = {"result_count": 42}
    cms.search_providers.return_value = [{"id": 1}, {"id": 2}]
    hrsa.get_state_workforce.return_value = {"urban_rural_split": {"urban": 0.7, "rural": 0.3}}
    medscape.get_compensation_survey.return_value = {
        "gender_split": {"male": 60, "female": 40},
        "practice_setting": {"hospital": 50, "private": 50}
    }

    return nppes, cms, hrsa, medscape

def test_build_distribution_with_state(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)

    result = builder.build_distribution(state="CA")

    assert result["practice_context"]["state"] == "CA"
    assert result["practice_context"]["nppes_providers"] == 42
    nppes.search_providers.assert_called_once_with(state="CA")


def test_build_distribution_no_state(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)

    result = builder.build_distribution()

    assert result["practice_context"]["state"] is None
    assert result["practice_context"]["nppes_providers"] == 42
    nppes.search_providers.assert_called_once_with(state=None)

def test_build_distribution_empty_nppes(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    nppes.search_providers.return_value = {} 
    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)

    result = builder.build_distribution(state="NY")

    assert result["practice_context"]["nppes_providers"] == 0


def test_build_distribution_nppes_exception(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    nppes.search_providers.side_effect = HTTPError("API error")
    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)

   
    with pytest.raises(HTTPError):
        builder.build_distribution(state="TX")