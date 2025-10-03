import json
from typing import Dict, Any, List
import numpy as np

RNG = np.random.default_rng()

ATTR_ORDER = [
    ("gender", ["male", "female"]),
    ("age_band", ["25-34", "35-44", "45-54", "55-64", "65+"]),
    ("urbanicity", ["urban", "suburban", "rural"]),
    ("practice_setting", ["academic", "community", "private"]),
    ("state", ["CA", "TX", "NY", "FL", "PA", "IL", "OH", "GA", "NC", "MI", "Other"]),
    ("years_in_practice", ["0-5", "6-10", "11-20", "21-30", "31+"]),
    ("board_certified", ["true", "false"]),
]

BEHAVIOR_RULES = {
    "academic": {"guideline_adherence": (0.7, 0.95), "innovation_openness": (0.6, 0.95)},
    "community": {"guideline_adherence": (0.55, 0.85), "innovation_openness": (0.45, 0.8)},
    "private": {"guideline_adherence": (0.5, 0.8), "innovation_openness": (0.4, 0.75)},
    "urban": {"access_constraint": (0.1, 0.4)},
    "suburban": {"access_constraint": (0.2, 0.5)},
    "rural": {"access_constraint": (0.4, 0.8)},
}

class PersonaGenerator:
    def __init__(self, json_file : str = 'sample_distribution.json'):
        with open(json_file, "r") as f:
            self.distributions = json.load(f)

    def _sample_from_probs(self, options: List[str], probs_dict: Dict[str, float]) -> str:
        weights = np.array([probs_dict.get(opt, 0.0) for opt in options], dtype=float)
        weights = weights / weights.sum()
        idx = RNG.choice(len(options), p=weights)
        return options[idx]

    def _generate_persona(self, idx: int) -> Dict[str, Any]:
        sel = {attr: self._sample_from_probs(opts, self.distributions[attr]) for attr, opts in ATTR_ORDER}

        yip_map = {
            "0-5": RNG.integers(0, 6),
            "6-10": RNG.integers(6, 11),
            "11-20": RNG.integers(11, 21),
            "21-30": RNG.integers(21, 31),
            "31+": RNG.integers(31, 41),
        }

        demographics = {
            "gender": sel["gender"],
            "age_band": sel["age_band"],
            "state": sel["state"],
            "urbanicity": sel["urbanicity"],
        }

        practice = {
            "setting": sel["practice_setting"],
            "years_in_practice": int(yip_map[sel["years_in_practice"]]),
            "board_certified": sel["board_certified"] == "true",
            "fellowship": "Pulmonary & Critical Care"
        }

        setting, urb = practice["setting"], demographics["urbanicity"]

        def _rand(a: float, b: float) -> float:
            return round(float(RNG.uniform(a, b)), 2)

        attitudes = {
            "guideline_adherence": _rand(*BEHAVIOR_RULES[setting]["guideline_adherence"]),
            "innovation_openness": _rand(*BEHAVIOR_RULES[setting]["innovation_openness"]),
            "access_constraint": _rand(*BEHAVIOR_RULES[urb]["access_constraint"]),
        }

        return {
            "persona_id": f"pulm_{idx:04d}",
            "demographics": demographics,
            "practice": practice,
            "attitudes": attitudes,
        }

    def generate_personas(self, n: int = 20, max_retries: int = 5) -> List[Dict[str, Any]]:
        personas, seen = [], set()
        for i in range(n):
            for _ in range(max_retries):
                p = self._generate_persona(i + 1)
                key = (
                    p["demographics"]["gender"],
                    p["demographics"]["age_band"],
                    p["demographics"]["state"],
                    p["demographics"]["urbanicity"],
                    p["practice"]["setting"],
                    p["practice"]["years_in_practice"],
                    p["practice"]["board_certified"]
                )
                if key not in seen:
                    seen.add(key)
                    personas.append(p)
                    break
            else:
                personas.append(p)
        return personas

    def save_personas(self, output_file: str, n: int = 20):
        personas = self.generate_personas(n)
        with open(output_file, "w") as f:
            json.dump(personas, f, indent=2)
        print(f"{len(personas)} personas saved to {output_file}")


# Usage example:
# generator = PersonaGenerator("population_distributions.json")
# generator.save_personas("person.json", n=50)
