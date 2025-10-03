from __future__ import annotations
import httpx
from typing import Dict, Any, Optional

CMS_MEDICARE_UTILIZATION_ENDPOINT = "https://data.cms.gov/data-api/v1/dataset/medicare-physician-utilization"

class CMSMedicareUtilizationClient:
    def __init__(self, base_url: str = CMS_MEDICARE_UTILIZATION_ENDPOINT, timeout: int = 60):
        self.client = httpx.Client(timeout=timeout)
        self.base_url = base_url

    def get_utilization(self, npi: str, year: str = "2022") -> Dict[str, Any]:
        params = {"npi": npi, "year": year}
        resp = self.client.get(self.base_url, params=params)
        print(resp,"99"*999)
        resp.raise_for_status()
        return resp.json()
    