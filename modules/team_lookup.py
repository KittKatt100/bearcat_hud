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
        "mascot": "Unknown Mascot ⚠️",
        "colors": "Not Verified ⚠️",
        "city": "Unknown ⚠️",
        "classification": "Unknown",
        "record": "N/A",
        "region_standing": "N/A",
        "recent_trends": "No data available",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title(),
        "county": county.title(),
        "state": state.title()
    }

def fill_missing_fields(data, school_name, county, state):
    filled = data.copy()
    fallback = fallback_data(school_name, county, state)
    for key, value in fallback.items():
        if key not in filled or filled[key] in ["", None]:
            filled[key] = value
    return filled

def find_school(state: str, county: str, school_name: str):
    state = state.lower()
    county = county.lower()
    school_name = school_name.lower()

    schools = load_school_metadata()
    try:
        school_data = schools[state][county][school_name]
        return fill_missing_fields(school_data, school_name, county, state)
    except KeyError:
        return fallback_data(school_name, county, state)
