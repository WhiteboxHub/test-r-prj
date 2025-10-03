from __future__ import annotations
import httpx
from typing import Dict, Any, Optional

HRSA_AHRF_ENDPOINT = "https://data.hrsa.gov/resource/ahrf.json"

class HRSAClient:
    def __init__(self, base_url: str = HRSA_AHRF_ENDPOINT, timeout: int = 30):
        self.client = httpx.Client(timeout=timeout)
        self.base_url = base_url

    def get_state_workforce(self, state: str, year: str = "2022") -> Dict[str, Any]:
        params = {"state": state, "year": year}
        resp = self.client.get(self.base_url, params=params)
        resp.raise_for_status()
        return resp.json()
    