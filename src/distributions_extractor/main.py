from clients.nppes_client import NPPESClient
from clients.cms_physician_compare_client import CMSPhysicianCompareClient
from clients.hrsa_client import HRSAClient
from clients.medscape_client import MedscapeClient
from distributions.pulmonologist_distribution_builder import PulmonologistDistributionBuilder

def run_example(state: str = "CA"):
    nppes = NPPESClient()
    cms = CMSPhysicianCompareClient()
    hrsa = HRSAClient()
    medscape = MedscapeClient()

    builder = PulmonologistDistributionBuilder(nppes, cms, hrsa, medscape)
    distribution = builder.build_distribution(state=state)

    print(distribution)

if __name__ == "__main__":
    run_example("CA")