import os
import json
import requests
from bs4 import BeautifulSoup

DATA_PATH = os.path.join("data", "schools.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def find_school(state, county, school):
    state = state.strip().lower()
    county = county.strip().lower()
    school = school.strip().lower()

    try:
        with open(DATA_PATH, "r") as file:
            school_data = json.load(file)
    except FileNotFoundError:
        return {"error": "schools.json not found."}

    for record in school_data.get("schools", []):
        if (
            record.get("state", "").lower() == state and
            record.get("county", "").lower() == county and
            record.get("school", "").lower() == school
        ):
            return record

    return fetch_school_info_from_web(state, county, school)

def fetch_school_info_from_web(state, county, school):
    query = f"{school} High School {county} County {state} mascot colors site:.edu OR site:.org OR site:.k12.{state.lower()}.us"
    search_url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"

    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.find_all("a", class_="result__a")
        first_link = results[0]["href"] if results else None

        if first_link:
            web_data = scrape_school_info(first_link)
            return {
                "school": school.title(),
                "county": county.title(),
                "state": state.upper(),
                "mascot": web_data.get("mascot", "Info Not Available"),
                "colors": web_data.get("colors", "Info Not Available"),
                "logo": web_data.get("logo", "https://via.placeholder.com/150x150.png?text=Mascot"),
                "city": web_data.get("city", "Info Not Available"),
                "classification": "Info Not Available",
                "record": "Info Not Available",
                "region_standing": "Info Not Available",
                "recent_trends": "Info Not Available"
            }

    except Exception as e:
        print("DuckDuckGo fallback failed:", e)

    return {
        "school": school.title(),
        "county": county.title(),
        "state": state.upper(),
        "mascot": "Info Not Available",
        "colors": "Info Not Available",
        "logo": "https://via.placeholder.com/150x150.png?text=Mascot",
        "city": "Info Not Available",
        "classification": "Info Not Available",
        "record": "Info Not Available",
        "region_standing": "Info Not Available",
        "recent_trends": "Info Not Available"
    }

def scrape_school_info(url):
    try:
        page = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")
        text = soup.get_text(separator=" ").lower()

        mascot = extract_snippet(text, "mascot")
        colors = extract_snippet(text, "colors")

        return {
            "mascot": mascot,
            "colors": colors,
            "city": "Info Not Available",
            "logo": "https://via.placeholder.com/150x150.png?text=Mascot"
        }

    except Exception as e:
        print("Error scraping school info:", e)
        return {}

def extract_snippet(text, keyword, radius=50):
    index = text.find(keyword)
    if index == -1:
        return "Info Not Available"
    start = max(0, index - radius)
    end = min(len(text), index + radius)
    snippet = text[start:end].strip().replace("\n", " ")
    return snippet if snippet else "Info Not Available"
