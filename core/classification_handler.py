import os
import json

CLASSIFICATION_PATH = "data/classification_map.json"

def load_classification_map():
    if not os.path.exists(CLASSIFICATION_PATH):
        return {}
    with open(CLASSIFICATION_PATH, "r") as f:
        return json.load(f)

def get_classification(state: str, county: str, school_name: str) -> str:
    state = state.lower().strip()
    county = county.lower().strip()
    school_name = school_name.lower().strip()

    classification_data = load_classification_map()

    try:
        return classification_data[state][county][school_name]["classification"]
    except KeyError:
        return "Info Not Available"

