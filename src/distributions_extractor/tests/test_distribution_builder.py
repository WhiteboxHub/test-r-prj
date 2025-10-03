import pytest
from unittest.mock import MagicMock
from src.distributions_extractor.clients.nppes_client import NPPESClient
from src.distributions_extractor.clients.cms_physician_compare_client import CMSPhysicianCompareClient
from src.distributions_extractor.clients.hrsa_client import HRSAClient
from src.distributions_extractor.clients.medscape_client import MedscapeClient
from src.distributions_extractor.distributions.pulmonologist_distribution_builder import PulmonologistDistributionBuilder


@pytest.fixture
def mock_clients():
    """Return mocked clients for testing."""
    nppes = MagicMock(spec=NPPESClient)
    cms = MagicMock(spec=CMSPhysicianCompareClient)
    hrsa = MagicMock(spec=HRSAClient)
    medscape = MagicMock(spec=MedscapeClient)
    return nppes, cms, hrsa, medscape


def test_build_distribution_with_providers(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    nppes.search_providers.return_value = {"result_count": 42}

    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)
    result = builder.build_distribution(state="CA")

    assert result["practice_context"]["state"] == "CA"
    assert result["practice_context"]["nppes_providers"] == 42


def test_build_distribution_no_providers(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    nppes.search_providers.return_value = {"result_count": 0}

    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)
    result = builder.build_distribution(state="TX")

    assert result["practice_context"]["state"] == "TX"
    assert result["practice_context"]["nppes_providers"] == 0


def test_build_distribution_missing_result_count(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    nppes.search_providers.return_value = {}

    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)
    result = builder.build_distribution(state="NY")

    assert result["practice_context"]["nppes_providers"] == 0


# Example future test when you enable other clients
@pytest.mark.skip(reason="Extended schema not implemented yet")
def test_build_distribution_with_all_sources(mock_clients):
    nppes, cms, hrsa, medscape = mock_clients
    nppes.search_providers.return_value = {"result_count": 100}
    cms.search_providers.return_value = [{"id": 1}, {"id": 2}]
    hrsa.get_state_workforce.return_value = {"urban_rural_split": {"urban": 0.7, "rural": 0.3}}
    medscape.get_compensation_survey.return_value = {
        "gender_split": {"male": 60, "female": 40},
        "practice_setting": {"hospital": 70, "private": 30}
    }

    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)
    result = builder.build_distribution(state="FL")

    assert result["demographics"]["gender"]["male"] == 60
    assert result["practice_context"]["cms_providers"] == 2


# # test for load_population_distributions
# import distributions_extractor.distribution_builder as builder_module

# def test_load_population_distributions(monkeypatch):
#     fake_data = {"foo": "bar"}

#     monkeypatch.setattr("json.loads", lambda _: fake_data)
#     result = builder_module.load_population_distributions()

#     assert result == fake_data

if __name__=="__main__":
    pytest.main([__file__])