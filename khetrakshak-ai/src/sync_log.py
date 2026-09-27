"""
sync_log.py

Local-first store for diagnosis reports, and the opportunistic-sync stub.

Every diagnosis is appended to a local, anonymized JSONL log immediately
(works fully offline). When the device detects connectivity -- e.g. Wi-Fi at
a Common Service Centre -- `sync_pending()` would push unsynced entries to a
block-level aggregation service that builds the outbreak heatmap. That
network call is stubbed here (this prototype never calls out to a server);
the local queuing logic is real and testable.
"""

import json
import os
import time
from typing import Dict, List

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "outbreak_log.jsonl")


def log_diagnosis(crop: str, disease_label: str, block: str = "unspecified") -> Dict:
    entry = {
        "timestamp": time.time(),
        "crop": crop,
        "disease_label": disease_label,
        "block": block,  # coarse location only -- no farmer-identifying data
        "synced": False,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def pending_entries() -> List[Dict]:
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        return [json.loads(line) for line in f if line.strip()]


def sync_pending(connectivity_available: bool) -> int:
    """
    Returns the number of entries that *would* sync. Network push is stubbed
    -- see module docstring. Marking entries synced is left as a follow-up
    for the real build once a server endpoint exists.
    """
    if not connectivity_available:
        return 0
    return len(pending_entries())
