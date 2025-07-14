import json
import os
import requests
from duckduckgo_search import ddg
from bs4 import BeautifulSoup

DATA_PATH = "data/schools.json"

def load_school_metadata():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def fallback_data(school_name, county, state):
    return {
        "mascot": "Unknown Mascot",
        "colors": "Black & White",
        "city": "Unknown",
        "classification": "Unknown",
        "record": "N/A",
        "region_standing": "N/A",
        "recent_trends": "No data available",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title(),
        "county": county.title(),
        "state": state.title(),
    }

def search_school_colors(school_name, county, state):
    query = f"{school_name} {county} County {state} high school colors site:.edu OR site:.org"
    results = ddg(query, max_results=5)
    for result in results:
        url = result.get("href")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ", strip=True).lower()
                if "color" in text:
                    for color_line in text.split("."):
                        if "color" in color_line:
                            return extract_colors_from_text(color_line)
        except Exception:
            continue
    return "Black & White"

def extract_colors_from_text(text):
    known_colors = [
        "black", "white", "blue", "gold", "green", "orange",
        "red", "silver", "maroon", "purple", "yellow", "gray", "brown"
    ]
    found = [color.title() for color in known_colors if color in text]
    return " & ".join(found) if found else "Black & White"

def find_school(state: str, county: str, school_name: str):
    state = state.lower()
    county = county.lower()
    school_name = school_name.lower()

    schools = load_school_metadata()
    try:
        school = schools[state][county][school_name]
        if school.get("colors", "Black & White") == "Black & White":
            updated_colors = search_school_colors(school_name, county, state)
            school["colors"] = updated_colors
        return school
    except KeyError:
        fallback = fallback_data(school_name, county, state)
        fallback["colors"] = search_school_colors(school_name, county, state)
        return fallback
