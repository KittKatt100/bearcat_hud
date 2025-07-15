import json
import os

HSAA_MAP_PATH = "data/hsaa_structure.json"

def load_hsaa_data():
    if not os.path.exists(HSAA_MAP_PATH):
        return {}
    with open(HSAA_MAP_PATH, "r") as f:
        return json.load(f)

def get_hsaa_affiliation(state: str) -> dict:
    """
    Returns governing body details for a given state, such as GHSA or FHSAA.
    """
    state = state.lower().strip()
    hsaa_data = load_hsaa_data()
    return hsaa_data.get(state, {
        "association": "Unknown",
        "playoff_structure": "Info Not Available",
        "season_start": "Info Not Available",
        "notes": "Info Not Available"
    })

