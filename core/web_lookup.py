import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

def get_school_web_data(school_name, county, state):
    query = f"{school_name} {county} County {state} high school mascot football record classification site:.edu OR site:.org"
    info = {
        "mascot": "Unknown",
        "city": "Unknown",
        "classification": "Unknown",
        "record": "Unknown",
        "region_standing": "Unknown",
        "recent_trends": "Unknown",
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

            # Attempt to extract mascot-like keywords
            text = soup.get_text(" ", strip=True).lower()
            mascots = ["tigers", "bulldogs", "rams", "wildcats", "gators", "patriots", "tornadoes"]
            for m in mascots:
                if m in text:
                    info["mascot"] = m.title()
                    break

            # Try to pull classification
            if "class" in text:
                split = text.split("class")
                if len(split) > 1:
                    after = split[1][:10].strip().split(" ")[0]
                    info["classification"] = after.upper().replace("-", "").replace(":", "").strip()

            # Try to infer record (look for X-Y or digits-w/l)
            import re
            record_match = re.search(r"\b(\d{1,2})[-–](\d{1,2})\b", text)
            if record_match:
                info["record"] = record_match.group(0)

            # Try to find school logo from images
            imgs = soup.find_all("img")
            for img in imgs:
                src = img.get("src", "")
                if any(keyword in src.lower() for keyword in ["logo", "mascot", "school"]):
                    if src.startswith("http"):
                        info["logo"] = src
                    else:
                        domain = url.split("/")[2]
                        info["logo"] = f"https://{domain}/{src.lstrip('/')}"
                    break

    except Exception as e:
        print("Web scrape failed:", e)

    return info
