import os
import json
from datetime import datetime

NOTES_FOLDER = "memory/coach_notes"

def _notes_path(school_name: str):
    filename = school_name.lower().replace(" ", "_") + ".json"
    return os.path.join(NOTES_FOLDER, filename)

def load_notes(school_name: str):
    path = _notes_path(school_name)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_notes(school_name: str, notes: dict):
    os.makedirs(NOTES_FOLDER, exist_ok=True)
    path = _notes_path(school_name)
    with open(path, "w") as f:
        json.dump(notes, f, indent=4)

def add_note(school_name: str, category: str, note_text: str):
    notes = load_notes(school_name)
    date_key = datetime.now().strftime("%Y-%m-%d")

    if category not in notes:
        notes[category] = {}

    if date_key not in notes[category]:
        notes[category][date_key] = []

    notes[category][date_key].append(note_text.strip())
    save_notes(school_name, notes)

def edit_note(school_name: str, category: str, date_key: str, index: int, new_text: str):
    notes = load_notes(school_name)
    try:
        notes[category][date_key][index] = new_text.strip()
        save_notes(school_name, notes)
        return True
    except (KeyError, IndexError):
        return False

