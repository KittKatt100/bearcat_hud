import json
import os

DATA_PATH = "data/schools.json"

def load_school_metadata():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def fallback_data(school_name, county, state):
    return {
        "mascot": "Unknown Mascot",
        "colors": "Black & White",
        "city": "Unknown",
        "classification": "Unknown",
        "record": "N/A",
        "region_standing": "N/A",
        "recent_trends": "No data available",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title(),
        "county": county.title(),
        "state": state.title()
    }

def find_school(state: str, county: str, school_name: str):
    state = state.lower()
    county = county.lower()
    school_name = school_name.lower()

    schools = load_school_metadata()
    try:
        return schools[state][county][school_name]
    except KeyError:
        return fallback_data(school_name, county, state)
