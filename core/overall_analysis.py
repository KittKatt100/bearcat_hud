import json
import os

ANALYSIS_PATH = "data/analysis"

def _analysis_file_path(school_name: str, county: str, state: str) -> str:
    slug = f"{school_name}_{county}_{state}".lower().replace(" ", "_")
    return os.path.join(ANALYSIS_PATH, f"{slug}.json")

def load_overall_analysis(school_name: str, county: str, state: str) -> dict:
    path = _analysis_file_path(school_name, county, state)
    if not os.path.exists(path):
        return {
            "identity": {},
            "offense": {},
            "quarterback": {},
            "oline": {},
            "skill": {},
            "formation": {},
            "scoring": {},
            "situational": {},
            "psych": {},
            "tells": {}
        }
    with open(path, "r") as f:
        return json.load(f)

def save_overall_analysis(school_name: str, county: str, state: str, data: dict):
    os.makedirs(ANALYSIS_PATH, exist_ok=True)
    path = _analysis_file_path(school_name, county, state)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
