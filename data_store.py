import os
import json

MEMORY_PATH = "memory/opponents"

def save_opponent_data(name, data):
    os.makedirs(MEMORY_PATH, exist_ok=True)
    with open(f"{MEMORY_PATH}/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

def load_opponent_data(name):
    try:
        with open(f"{MEMORY_PATH}/{name}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
