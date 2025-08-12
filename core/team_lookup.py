# core/team_lookup.py
import json
import os
from core.web_lookup import get_school_web_data

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLASS_MAP_PATH = os.path.join(DATA_DIR, "classification_map.json")

INFO_NA = "Info Not Available"

def _load_class_map():
    if not os.path.exists(CLASS_MAP_PATH):
        return {}
    with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CLASS_MAP = _load_class_map()

def _assoc_for_state(state_str: str):
    s = state_str.strip().upper()
    for key, meta in CLASS_MAP.items():
        if s == key.upper() or s == meta.get("abbr", "").upper():
            return meta
    return {"name": INFO_NA, "abbr": s, "levels": [], "notes": ""}

def _infer_classification(text: str, assoc_levels):
    if not text:
        return INFO_NA
    t = text.upper()
    candidates = []
    # Common patterns (A/AA/AAA etc. plus numeric tiers)
    for lvl in assoc_levels or []:
        if lvl.upper() in t:
            candidates.append(lvl)
    if "CLASS " in t:
        # crude pull like "CLASS 4A" or "CLASS AAA"
        part = t.split("CLASS ", 1)[1][:6].strip().split()[0]
        candidates.append(part)
    return candidates[0] if candidates else INFO_NA

def find_school(state: str, county: str, school_name: str) -> dict:
    # 1) quick web probe
    info = get_school_web_data(school_name, county, state)

    # 2) attach HS association metadata
    assoc = _assoc_for_state(state)
    info["association"] = assoc.get("name") or INFO_NA

    # 3) best-effort classification normalization
    info["classification"] = _infer_classification(
        info.get("classification"), assoc.get("levels")
    )

    # normalize blanks -> Info Not Available
    for k, v in list(info.items()):
        if not v or str(v).strip() == "" or str(v).strip().lower() in {"unknown", "n/a"}:
            info[k] = INFO_NA

    # echo back canonical names
    info["school_name"] = school_name.title()
    info["county"] = county.title()
    info["state"] = state.title()
    return info

