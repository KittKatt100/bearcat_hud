# core/web_lookup.py
"""
Best-effort web probe:
- Tries DuckDuckGo & simple page scrape to guess mascot/logo/record/city.
- Always returns a dict with fields filled or "Info Not Available".
- Stays resilient if packages or network aren’t available.
"""
INFO_NA = "Info Not Available"

def get_school_web_data(school_name: str, county: str, state: str) -> dict:
    data = {
        "mascot": INFO_NA,
        "colors": INFO_NA,
        "city": INFO_NA,
        "classification": INFO_NA,
        "record": INFO_NA,
        "region_standing": INFO_NA,
        "recent_trends": INFO_NA,
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
        "school_name": school_name.title(),
        "county": county.title(),
        "state": state.title()
    }

    # Lazy imports (so app still runs if these aren’t installed yet)
    try:
        import requests
        from duckduckgo_search import DDGS
        from bs4 import BeautifulSoup
    except Exception:
        return data  # keep app functional

    query = f'{school_name} {county} County {state} high school football site:.edu OR site:.k12.* OR site:.org'
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return data

        url = results[0].get("href") or results[0].get("url")
        if not url:
            return data

        html = requests.get(url, timeout=8).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)

        # Very light heuristics
        mascots = ["tigers","bulldogs","wildcats","gators","patriots","tornadoes",
                   "sharks","panthers","eagles","lions","hornets","crimson tide"]
        low = text.lower()
        for m in mascots:
            if f" {m} " in low or f"{m} football" in low:
                data["mascot"] = m.title()
                break

        # record like "10-2"
        import re
        m = re.search(r"\b(\d{1,2})[-–](\d{1,2})\b", text)
        if m:
            data["record"] = m.group(0)

        # city guess: look for “City of …” or address chunks
        cm = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)[, ]+\b" + state[:2] + r"\b", text)
        if cm:
            data["city"] = cm.group(1)

        # logo guess
        for img in soup.find_all("img"):
            src = (img.get("src") or "").strip()
            if not src:
                continue
            low_src = src.lower()
            if any(k in low_src for k in ["logo","mascot","seal","crest"]):
                if src.startswith("http"):
                    data["logo"] = src
                else:
                    # make absolute
                    from urllib.parse import urljoin
                    data["logo"] = urljoin(url, src)
                break

        return data
    except Exception:
        return data
