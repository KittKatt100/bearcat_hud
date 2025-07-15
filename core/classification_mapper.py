def map_hsaa_structure(state: str):
    """Return HSAA governing body, classification schema, and playoff structure for given state."""
    state = state.lower()
    hsaa_data = {
        "florida": {
            "association": "FHSAA (Florida High School Athletic Association)",
            "classification_model": "1A–4M (rural to metro)",
            "playoff_structure": "District champs + wildcard points; regional → state"
        },
        "georgia": {
            "association": "GHSA (Georgia High School Association)",
            "classification_model": "A-D1 to AAAAAAA",
            "playoff_structure": "Region champs + top seeds; 32-team brackets"
        },
        "alabama": {
            "association": "AHSAA (Alabama High School Athletic Association)",
            "classification_model": "1A–7A",
            "playoff_structure": "Top 4 per region; seeded brackets"
        },
        "texas": {
            "association": "UIL (University Interscholastic League)",
            "classification_model": "1A–6A + Division I/II splits",
            "playoff_structure": "District seeding into region/state brackets"
        },
        # Add more states here as needed
    }

    default = {
        "association": "Unknown HSAA",
        "classification_model": "Not Available",
        "playoff_structure": "Not Available"
    }

    return hsaa_data.get(state, default)
