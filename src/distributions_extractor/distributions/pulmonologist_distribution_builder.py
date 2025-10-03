from __future__ import annotations
from typing import Dict, Any, Optional
from distributions_extractor.clients.nppes_client import NPPESClient
from distributions_extractor.clients.cms_physician_compare_client import CMSPhysicianCompareClient
from distributions_extractor.clients.hrsa_client import HRSAClient
from distributions_extractor.clients.medscape_client import MedscapeClient
from requests import HTTPError
import json
class PulmonologistDistributionBuilder:
    def __init__(self, nppes: NPPESClient, cms: CMSPhysicianCompareClient, hrsa: HRSAClient, medscape: MedscapeClient):
        self.nppes = nppes
        self.cms = cms
        self.hrsa = hrsa
        self.medscape = medscape

    def build_distribution(self, state: Optional[str] = None) -> Dict[str, Any]:
        # try:
            # Pull from different sources
        nppes_data = self.nppes.search_providers(state=state)
        # cms_data = self.cms.search_providers(state=state)
        # hrsa_data = self.hrsa.get_state_workforce(state) if state else {}
        # medscape_data = self.medscape.get_compensation_survey()
            
        # Merge into JSON schema (example)


        

        return {
        "practice_context": {
            "state": state,
            "nppes_providers": nppes_data.get("result_count", 0),
        }
    }

        # return {
        #     "demographics": {
        #         "gender": medscape_data["gender_split"],
        #         "practice_setting": medscape_data["practice_setting"]
        #     },
        #     "practice_context": {
        #         "state": state,
        #         "cms_providers": len(cms_data),
        #         "nppes_providers": nppes_data.get("result_count", 0),
        #         "urban_vs_rural": hrsa_data.get("urban_rural_split", {"urban": 0.8, "rural": 0.2})
        #     }
        # }
          

def load_population_distributions():
    distribuion_data = json.loads('sample_distributions.json')
    return distribuion_data