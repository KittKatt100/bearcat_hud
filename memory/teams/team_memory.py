import os
import json

TEAM_FOLDER = "memory/teams"

def _team_path(team_name: str):
    return os.path.join(TEAM_FOLDER, f"{team_name.lower().replace(' ', '_')}.json")

def load_team_profile(team_name: str):
    path = _team_path(team_name)
    if not os.path.exists(path):
        # Return an empty template if the file doesn’t exist yet
        return {
            "team_name": team_name,
            "record": "0-0",
            "top_plays": [],
            "weaknesses": [],
            "avg_quarter_yards": {},
            "formations": {}
        }
    with open(path, "r") as f:
        return json.load(f)

def save_team_profile(team_name: str, data: dict):
    os.makedirs(TEAM_FOLDER, exist_ok=True)
    path = _team_path(team_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
