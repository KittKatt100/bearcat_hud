# bearcat_hud/core/web_lookup.py
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

INFO_NA = "Info Not Available"

def get_school_web_data(school_name: str, county: str, state: str) -> dict:
    query = f'{school_name} {county} County {state} high school football site:.edu OR site:.org'
    info = {
        "mascot": INFO_NA,
        "colors": INFO_NA,
        "city": INFO_NA,
        "classification": INFO_NA,
        "record": INFO_NA,
        "region_standing": INFO_NA,
        "recent_trends": INFO_NA,
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "raw_text": ""
    }

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return info

        # take the first plausible result
        url = results[0].get("href") or results[0].get("url") or results[0].get("link")
        if not url:
            return info

        html = requests.get(url, timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        info["raw_text"] = text

        low = text.lower()

        # very light heuristics (we’ll refine later)
        for m in ["tigers","sharks","wildcats","gators","patriots","tornadoes","bulldogs","panthers","lions","eagles"]:
            if f" {m} " in low:
                info["mascot"] = m.title()
                break

        # record like 10-2
        import re
        m = re.search(r"\b(\d{1,2})[-–](\d{1,2})\b", low)
        if m:
            info["record"] = f"{m.group(1)}-{m.group(2)}"

        # city guess: “City of X”, or “, FL” style
        m = re.search(r"\bCity of ([A-Za-z\.\-\' ]+)\b", text)
        if m:
            info["city"] = m.group(1).strip()

        # logo guess
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if any(k in (src or "").lower() for k in ["logo","mascot","athletic","athletics"]):
                if src.startswith("http"):
                    info["logo"] = src
                else:
                    from urllib.parse import urljoin
                    info["logo"] = urljoin(url, src)
                break

    except Exception as e:
        # keep it quiet in prod; fine to print while you’re testing
        print("Web lookup failed:", e)

    return info
