import os
import json

def load_team_profile(team_name: str):
    file_path = f"memory/teams/{team_name.lower()}.json"
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

def save_team_profile(team_name: str, data: dict):
    file_path = f"memory/teams/{team_name.lower()}.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

