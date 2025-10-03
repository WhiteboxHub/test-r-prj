from __future__ import annotations
import httpx
from typing import Dict, Any, Optional

class MedscapeClient:
    def __init__(self):
        # No public API; either scrape or maintain as static dataset
        pass

    def get_compensation_survey(self, specialty: str = "Pulmonology") -> Dict[str, Any]:
        # Static JSON or scraped data
        return {
            "specialty": specialty,
            "avg_income": 310000,
            "gender_split": {"male": 0.70, "female": 0.30},
            "practice_setting": {"academic": 0.25, "community": 0.65, "other": 0.10}
        }
    