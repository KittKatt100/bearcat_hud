import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import re

def get_school_web_data(school_name, county, state):
    query = f"{school_name} {county} County {state} high school mascot football record classification site:.edu OR site:.org"
    info = {
        "mascot": "Info Not Available",
        "city": "Info Not Available",
        "classification": "Info Not Available",
        "record": "Info Not Available",
        "region_standing": "Info Not Available",
        "recent_trends": "Info Not Available",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title(),
        "county": county.title(),
        "state": state.title()
    }

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return info

            url = results[0]["href"]
            html = requests.get(url, timeout=8).text
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(" ", strip=True).lower()

            # Attempt to extract mascot from known patterns
            mascots = ["tigers", "bulldogs", "rams", "wildcats", "gators", "patriots", "tornadoes"]
            for m in mascots:
                if m in text:
                    info["mascot"] = m.title()
                    break

            # Attempt to extract classification
            if "class" in text:
                split = text.split("class")
                if len(split) > 1:
                    after = split[1][:10].strip().split(" ")[0]
                    classification = after.upper().replace("-", "").replace(":", "").strip()
                    if classification:
                        info["classification"] = classification

            # Attempt to extract record
            record_match = re.search(r"\b(\d{1,2})[-–](\d{1,2})\b", text)
            if record_match:
                info["record"] = record_match.group(0)

            # Attempt to find logo or mascot image
            imgs = soup.find_all("img")
            for img in imgs:
                src = img.get("src", "")
                if any(k in src.lower() for k in ["logo", "mascot", "school"]):
                    if src.startswith("http"):
                        info["logo"] = src
                    else:
                        domain = url.split("/")[2]
                        info["logo"] = f"https://{domain}/{src.lstrip('/')}"
                    break

    except Exception as e:
        print("Web scrape failed:", e)

    return info
