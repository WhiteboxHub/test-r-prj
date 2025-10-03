
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

HERE = Path(__file__).parent

def load_population_distributions(path: Path | str | None = None) -> Dict[str, Any]:
    if path is None:
        path = HERE / "sample_distributions.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
