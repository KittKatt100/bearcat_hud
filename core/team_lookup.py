# bearcat_hud/core/team_lookup.py
import json
import os
from bearcat_hud.core.web_lookup import get_school_web_data

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLASS_MAP_PATH = os.path.join(DATA_DIR, "classification_map.json")
INFO_NA = "Info Not Available"

def _load_class_map():
    if not os.path.exists(CLASS_MAP_PATH):
        return {}
    with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CLASS_MAP = _load_class_map()

def _assoc_for_state(state_str: str) -> dict:
    s = (state_str or "").strip().upper()
    for key, meta in CLASS_MAP.items():
        if s == key.upper() or s == (meta.get("abbr", "")).upper():
            return meta
    return {"name": INFO_NA, "abbr": s, "levels": [], "notes": ""}

def _infer_classification(text: str, assoc_levels) -> str:
    if not text:
        return INFO_NA
    t = text.upper()
    # try level keywords (descending priority)
    for level in assoc_levels or []:
        if level.upper() in t:
            return level
    # very loose capture like "CLASS 4A"
    import re
    m = re.search(r"\bCLASS\s*([0-9A-Z-]+)\b", t)
    if m:
        return m.group(0).replace("  ", " ").strip()
    return INFO_NA

def find_school(state: str, county: str, school_name: str) -> dict:
    meta = get_school_web_data(school_name, county, state)

    assoc = _assoc_for_state(state)
    if meta.get("classification") in (None, "", "Unknown", INFO_NA):
        meta["classification"] = _infer_classification(meta.get("raw_text", ""), assoc.get("levels"))

    # standardize blanks to Info Not Available
    for k in ["mascot","colors","city","classification","record","region_standing","recent_trends","logo"]:
        v = meta.get(k)
        if not v or str(v).strip().lower() in {"unknown","n/a","placeholder"}:
            meta[k] = INFO_NA if k != "logo" else "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"

    meta["school_name"] = school_name.title()
    meta["county"] = county.title()
    meta["state"] = state.title()
    return meta
