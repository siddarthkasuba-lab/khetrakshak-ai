"""
scheme_matcher.py

Looks up government subsidy / insurance schemes relevant to a diagnosed
disease from a locally cached database (data/schemes.json). No network
call -- this is the "Connect" step in the offline pipeline.
"""

import json
import os
from typing import List, Dict

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "schemes.json")


def _load_schemes() -> List[Dict]:
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def matching_schemes(disease_label: str) -> List[Dict]:
    schemes = _load_schemes()
    return [s for s in schemes if disease_label in s.get("applies_to_diseases", [])]
