import json
import random
from pathlib import Path
from typing import Dict, Any, List


class PersonaGenerator:
    def __init__(self, distribution: Dict[str, Any]):
        self.distribution = distribution

    def _sample_from_distribution(self, dist: Dict[str, float]) -> str:
        """Weighted random choice from a distribution dict."""
        options, weights = zip(*dist.items())
        return random.choices(options, weights=weights, k=1)[0]

    def generate_persona(self, idx: int) -> Dict[str, Any]:
        """Generate a single persona using distributions."""
        demo = self.distribution["demographics"]
        context = self.distribution["practice_context"]
        treatment = self.distribution["treatment_patterns"]

        persona = {
            "id": f"pulmonologist_{idx+1}",
            "age": self._sample_from_distribution(demo["age"]),
            "gender": self._sample_from_distribution(demo["gender"]),
            "state": self._sample_from_distribution(demo["state_distribution"]),
            "practice_setting": self._sample_from_distribution(demo["practice_setting"]),
            "urban_rural": self._sample_from_distribution(context["urban_vs_rural"]),
            "patient_mix": self._sample_from_distribution(context["patient_mix"]),
            "copd_volume": self._sample_from_distribution(context["copd_patient_volume"]),
            "guideline_adherence": self._sample_from_distribution(treatment["guideline_adherence"]),
            "preferred_initial_therapy": self._sample_from_distribution(treatment["preferred_initial_therapy"]),
            "biologic_adoption": self._sample_from_distribution(treatment["biologic_adoption"])
        }
        return persona

    def generate_personas(self, n: int = 20) -> List[Dict[str, Any]]:
        return [self.generate_persona(i) for i in range(n)]

    def save_personas(self, output_file: Path, n: int = 20):
        personas = self.generate_personas(n)
        output_file.write_text(json.dumps(personas, indent=2))
        print(f"✅ Saved {n} personas to {output_file}")