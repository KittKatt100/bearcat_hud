import json
import os
from core.web_lookup import get_school_web_data

DATA_PATH = "data/schools.json"

def load_school_metadata():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_school_metadata(schools):
    with open(DATA_PATH, "w") as f:
        json.dump(schools, f, indent=2)

def find_school(state, county, school_name):
    state_key = state.lower()
    county_key = county.lower()
    school_key = school_name.lower()

    schools = load_school_metadata()

    if state_key in schools and county_key in schools[state_key] and school_key in schools[state_key][county_key]:
        return schools[state_key][county_key][school_key]

    # If not found, use web lookup
    data = get_school_web_data(school_name, county, state)

    # Save to local memory
    if state_key not in schools:
        schools[state_key] = {}
    if county_key not in schools[state_key]:
        schools[state_key][county_key] = {}
    schools[state_key][county_key][school_key] = data
    save_school_metadata(schools)

    return data
