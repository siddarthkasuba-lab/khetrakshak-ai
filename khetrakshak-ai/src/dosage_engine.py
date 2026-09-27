"""
dosage_engine.py

Deterministic, rules-based treatment + dosage lookup.

Intentionally NOT model/LLM-driven: dosage recommendations are something a
farmer will physically act on, so they come from a fixed, auditable table
(data/treatments.json) scaled by field area, rather than generated text.
"""

import json
import os
from dataclasses import dataclass
from typing import Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "treatments.json")


@dataclass
class TreatmentPlan:
    disease_label: str
    display_name: str
    organic_product: Optional[str]
    organic_total_dose: Optional[str]
    organic_frequency: Optional[str]
    chemical_product: Optional[str]
    chemical_total_dose: Optional[str]
    chemical_frequency: Optional[str]
    notes: str


def _load_treatments() -> dict:
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def _scale(entry: Optional[dict], field_area_acres: float) -> tuple:
    if not entry:
        return None, None, None
    for unit_key, unit_label in (("dose_per_acre_l", "L"), ("dose_per_acre_kg", "kg"), ("dose_per_acre_g", "g")):
        if unit_key in entry:
            total = entry[unit_key] * field_area_acres
            return entry["product"], f"{total:.2f} {unit_label} total ({entry[unit_key]} {unit_label}/acre)", entry["frequency"]
    return entry.get("product"), None, entry.get("frequency")


def get_treatment_plan(disease_label: str, field_area_acres: float) -> TreatmentPlan:
    treatments = _load_treatments()
    entry = treatments.get(disease_label, treatments["healthy"])

    organic_product, organic_dose, organic_freq = _scale(entry.get("organic"), field_area_acres)
    chemical_product, chemical_dose, chemical_freq = _scale(entry.get("chemical"), field_area_acres)

    return TreatmentPlan(
        disease_label=disease_label,
        display_name=entry["display_name"],
        organic_product=organic_product,
        organic_total_dose=organic_dose,
        organic_frequency=organic_freq,
        chemical_product=chemical_product,
        chemical_total_dose=chemical_dose,
        chemical_frequency=chemical_freq,
        notes=entry.get("notes", ""),
    )
