# core/analysis_loader.py
import json
import os
from slugify import slugify

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ANALYSIS_DIR = os.path.join(DATA_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

def make_slug(school: str, county: str, state: str) -> str:
    base = f"{school}-{county}-{state}"
    return slugify(base)

def save_analysis(slug: str, analysis: dict) -> str:
    path = os.path.join(ANALYSIS_DIR, f"{slug}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    return path
