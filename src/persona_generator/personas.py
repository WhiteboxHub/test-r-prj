
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import numpy as np
from src.extract_distributions.distributions import load_population_distributions

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

def _sample_from_probs(options: List[str], probs_dict: Dict[str, float]) -> str:
    import numpy as np
    weights = np.array([probs_dict.get(opt, 0.0) for opt in options], dtype=float)
    weights = weights / weights.sum()
    idx = RNG.choice(len(options), p=weights)
    return options[idx]

def generate_persona(distributions: Dict[str, Dict[str, float]], idx: int) -> Dict[str, Any]:
    sel = {attr: _sample_from_probs(opts, distributions[attr]) for attr, opts in ATTR_ORDER}
    yip_map = {"0-5": RNG.integers(0, 6), "6-10": RNG.integers(6, 11), "11-20": RNG.integers(11, 21),
               "21-30": RNG.integers(21, 31), "31+": RNG.integers(31, 41)}
    demographics = {"gender": sel["gender"], "age_band": sel["age_band"], "state": sel["state"], "urbanicity": sel["urbanicity"]}
    practice = {"setting": sel["practice_setting"], "years_in_practice": int(yip_map[sel["years_in_practice"]]),
                "board_certified": True if sel["board_certified"] == "true" else False, "fellowship": "Pulmonary & Critical Care"}
    setting, urb = practice["setting"], demographics["urbanicity"]
    def _rand(a: float, b: float) -> float: return round(float(RNG.uniform(a, b)), 2)
    attitudes = {"guideline_adherence": _rand(*BEHAVIOR_RULES[setting]["guideline_adherence"]),
                 "innovation_openness": _rand(*BEHAVIOR_RULES[setting]["innovation_openness"]),
                 "access_constraint": _rand(*BEHAVIOR_RULES[urb]["access_constraint"])}
    return {"persona_id": f"pulm_{idx:04d}", "demographics": demographics, "practice": practice, "attitudes": attitudes}

def sample_personas(n: int = 20, distributions: Dict[str, Dict[str, float]] | None = None, max_retries: int = 5):
    if distributions is None:
        distributions = load_population_distributions()
    personas, seen = [], set()
    for i in range(n):
        for _ in range(max_retries):
            p = generate_persona(distributions, i + 1)
            key = (p["demographics"]["gender"], p["demographics"]["age_band"], p["demographics"]["state"],
                   p["demographics"]["urbanicity"], p["practice"]["setting"], p["practice"]["years_in_practice"],
                   p["practice"]["board_certified"])
            if key not in seen:
                seen.add(key); personas.append(p); break
        else:
            personas.append(p)
    return personas
