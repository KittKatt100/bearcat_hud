import os
import json
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import ddg

DATA_PATH = "data/schools.json"

def load_school_metadata():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def extract_between_keywords(text, start_keywords, end_keywords):
    for start in start_keywords:
        start_index = text.find(start)
        if start_index != -1:
            sub_text = text[start_index + len(start):]
            for end in end_keywords:
                end_index = sub_text.find(end)
                if end_index != -1:
                    return sub_text[:end_index].strip().title()
    return None

def fetch_school_info_from_web(school_name, county, state):
    query = f"{school_name} High School {county} County {state} mascot and school colors"
    results = ddg(query, max_results=1)
    
    if not results:
        return "Unknown Mascot", "Unknown Colors", "Unknown City"

    url = results[0]['href']
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        return "Unknown Mascot", "Unknown Colors", "Unknown City"

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text().lower()

    mascot = extract_between_keywords(page_text, ["mascot is", "mascot:"], ["\n", ".", ","])
    colors = extract_between_keywords(page_text, ["colors are", "school colors", "colors:"], ["\n", ".", ","])
    city = extract_between_keywords(page_text, ["located in", "city of"], ["\n", ".", ","])

    return (
        mascot or "Unknown Mascot",
        colors or "Unknown Colors",
        city or "Unknown City"
    )

def fallback_data(school_name, county, state):
    mascot, colors, city = fetch_school_info_from_web(school_name, county, state)
    return {
        "mascot": mascot,
        "colors": colors,
        "city": city,
        "classification": "Unknown",
        "record": "N/A",
        "region_standing": "N/A",
        "recent_trends": "No data available",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title(),
        "county": county.title(),
        "state": state.title()
    }

def find_school(state: str, county: str, school_name: str):
    state = state.lower()
    county = county.lower()
    school_name = school_name.lower()

    schools = load_school_metadata()
    try:
        return schools[state][county][school_name]
    except KeyError:
        return fallback_data(school_name, county, state)
