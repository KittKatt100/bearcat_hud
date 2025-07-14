import os
import json

ANALYSIS_DIR = "data/analysis"

def get_analysis_path(school_name: str, county: str, state: str) -> str:
    school_file = f"{school_name.lower().replace(' ', '_')}_{county.lower().replace(' ', '_')}_{state.lower().replace(' ', '_')}.json"
    return os.path.join(ANALYSIS_DIR, school_file)

def load_overall_analysis(school_name: str, county: str, state: str) -> dict:
    path = get_analysis_path(school_name, county, state)

    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    
    # If no analysis found, return default structure
    return {
        "Opponent Identity": "No data available.",
        "Offensive Philosophy Summary": "No data available.",
        "Quarterback Profile": "No data available.",
        "Offensive Line Evaluation": "No data available.",
        "Skill Player Impact Review": "No data available.",
        "Formational DNA": "No data available.",
        "Scoring Patterns and Game Flow": "No data available.",
        "Situational Awareness": "No data available.",
        "Psychological and Team Culture Profile": "No data available.",
        "Tells and Tactical Cues": "No data available."
    }
