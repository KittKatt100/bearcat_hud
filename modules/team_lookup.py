import json
import os

DATA_PATH = "data/schools.json"

def load_school_metadata():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def find_school(state: str, county: str, school_name: str):
    state = state.lower()
    county = county.lower()
    school_name = school_name.lower()

    schools = load_school_metadata()
    try:
        return schools[state][county][school_name]
    except KeyError:
        return None
