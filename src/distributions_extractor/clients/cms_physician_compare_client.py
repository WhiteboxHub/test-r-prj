from __future__ import annotations
import httpx
from typing import Dict, Any, Optional

CMS_COMPARE_ENDPOINT = "https://data.cms.gov/provider-data/api/1/datastore/query/physician-compare-dataset/0"

class CMSPhysicianCompareClient:
    def __init__(self, base_url: str = CMS_COMPARE_ENDPOINT, timeout: int = 60):
        self.client = httpx.Client(timeout=timeout)
        self.base_url = base_url

    def search_providers(self, specialty: str = "Pulmonary Disease", state: Optional[str] = None, limit: int = 200) -> Dict[str, Any]:
        params = {"$limit": limit, "$q": specialty}
        if state:
            params["state"] = state
        resp = self.client.get(self.base_url, params=params)
        resp.raise_for_status()
        return resp.json()