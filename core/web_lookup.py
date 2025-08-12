# core/web_lookup.py
import requests
from bs4 import BeautifulSoup

INFO_NA = "Info Not Available"

try:
    # Optional – if not available, we still return safe defaults
    from duckduckgo_search import DDGS
    DUCK_OK = True
except Exception:
    DUCK_OK = False

def _safe_defaults(school_name, county, state):
    return {
        "mascot": INFO_NA,
        "colors": INFO_NA,
        "city": INFO_NA,
        "classification": INFO_NA,
        "record": INFO_NA,
        "region_standing": INFO_NA,
        "recent_trends": INFO_NA,
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title() if school_name else INFO_NA,
        "county": county.title() if county else INFO_NA,
        "state": state.title() if state else INFO_NA,
    }

def get_school_web_data(school_name: str, county: str, state: str) -> dict:
    """
    Light, failure-safe web look-up. If search/scrape fails, returns defaults.
    """
    base = _safe_defaults(school_name, county, state)

    if not DUCK_OK:
        return base

    try:
        query = f'{school_name} {county} County {state} high school mascot site:.edu OR site:.org'
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return base

        url = results[0].get("href") or results[0].get("url") or ""
        if not url:
            return base

        html = requests.get(url, timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True).lower()

        # try mascot
        mascots = ["tigers","bulldogs","rams","wildcats","gators","patriots","tornadoes","bearcats","hornets","warriors","pirates","panthers"]
        for m in mascots:
            if m in text:
                base["mascot"] = m.title()
                break

        # crude classification sniff
        if "class " in text:
            after = text.split("class ", 1)[1][:8]
            base["classification"] = after.upper().split()[0].replace(":", "")

        # crude city guess (if a header tag holds city/state)
        for tag in soup.find_all(["h1","h2","h3"]):
            t = (tag.get_text(" ", strip=True) or "").strip()
            if state.lower() in t.lower():
                base["city"] = t.replace(state, "").strip(" ,–-")
                break

        # logo hunt
        for img in soup.find_all("img"):
            src = img.get("src","")
            if any(k in (src or "").lower() for k in ["logo","mascot","seal"]):
                if src.startswith("http"):
                    base["logo"] = src
                else:
                    domain = url.split("/")[2]
                    base["logo"] = f"https://{domain}/{src.lstrip('/')}"
                break

        return base
    except Exception:
        return base
