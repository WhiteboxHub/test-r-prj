
from __future__ import annotations
import httpx
from typing import Dict, Any, Optional

NPPES_ENDPOINT = "https://npiregistry.cms.hhs.gov/api/"

class NPPESClient:
    def __init__(self, base_url: str = NPPES_ENDPOINT, timeout: int = 30):
        self.base_url = base_url.rstrip('/') + '/'
        self.client = httpx.Client(timeout=timeout)

    def search_providers(self, taxonomy: str = "207RP1001X", state: Optional[str] = None, limit: int = 200,city: str = "Los Angeles",) -> Dict[str, Any]:
        params = {"version": "2.1", "taxonomy": taxonomy, "limit": limit}
        if state:
            params["state"] = state
        if city:
            params["city"] = city

        resp = self.client.get(self.base_url, params=params)
        print(self.base_url, params) 
        resp.raise_for_status()
        return resp.json()