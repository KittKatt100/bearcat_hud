# core/team_lookup.py
import json, os, re
from core.web_lookup import get_school_web_data

INFO_NA = "Info Not Available"

DATA_DIR       = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLASS_MAP_PATH = os.path.join(DATA_DIR, "classification_map.json")

def _load_class_map():
    if not os.path.exists(CLASS_MAP_PATH):
        return {}
    with open(CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CLASS_MAP = _load_class_map()

def _assoc_for_state(state_str: str):
    s = (state_str or "").strip().upper()
    for key, meta in CLASS_MAP.items():
        if s == key.upper() or s == meta.get("abbr","").upper():
            return meta
    return {"name": INFO_NA, "abbr": s, "levels": [], "notes": ""}

def _infer_classification(text: str, assoc_levels):
    if not text:
        return INFO_NA
    t = text.upper()
    # Try to match known levels for the association
    for lvl in assoc_levels or []:
        if lvl.upper() in t:
            return lvl
    # Generic Class 1A, 2A, 3A...
    m = re.search(r"\b(1A|2A|3A|4A|5A|6A|7A|8A|A|AA|AAA|AAAA|AAAAA|AAAAAA|AAAAAAA)\b", t)
    if m:
        return m.group(1)
    return INFO_NA

def _normalize(d: dict):
    # Guarantee keys and fill missing with INFO_NA
    keys = ["mascot","colors","city","classification","record","region_standing","recent_trends",
            "logo","school_name","county","state"]
    out = {}
    for k in keys:
        v = d.get(k)
        if not v or str(v).strip()=="":
            v = INFO_NA
        out[k] = v
    return out

def find_school(state: str, county: str, school_name: str) -> dict:
    state  = (state or "").strip()
    county = (county or "").strip()
    school = (school_name or "").strip()

    # 1) Try the web (safe, with fallbacks)
    info = get_school_web_data(school, county, state)

    # 2) Attach association context + try improve classification
    assoc = _assoc_for_state(state)
    if info.get("classification") in (None, "", "Unknown", INFO_NA):
        guessed = _infer_classification(" ".join([str(v) for v in info.values()]), assoc.get("levels", []))
        info["classification"] = guessed

    # 3) Ensure naming/casing is consistent
    info["school_name"] = school.title() if school else INFO_NA
    info["county"]      = county.title() if county else INFO_NA
    info["state"]       = state.title() if state else INFO_NA

    return _normalize(info)
