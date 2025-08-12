# core/overall_analysis.py
from datetime import datetime

INFO_NA = "Info Not Available"

def build_overall_analysis(team: dict) -> dict:
    """
    Produces a structured Overall Team Analysis object from the quick intel.
    This is the foundation you’ll expand as you add stats, film, play-by-play, etc.
    """
    def v(key):  # normalized fetch
        val = (team or {}).get(key)
        if not val or str(val).strip().lower() in {"unknown", "n/a", "info not available"}:
            return INFO_NA
        return val

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "opponent": {
            "school": v("school_name"),
            "county": v("county"),
            "state": v("state"),
            "association": v("association"),
            "classification": v("classification"),
            "mascot": v("mascot"),
            "colors": v("colors"),
            "city": v("city"),
            "logo": v("logo"),
            "record": v("record"),
            "region_standing": v("region_standing"),
            "recent_trends": v("recent_trends"),
        },
        "identity_summary": {
            "offensive_philosophy": INFO_NA,
            "tempo_tendencies": INFO_NA,
            "use_of_motion_shifts": INFO_NA
        },
        "quarterback_profile": {
            "tools": INFO_NA,
            "progressions": INFO_NA,
            "scramble_rate": INFO_NA,
            "under_pressure": INFO_NA
        },
        "offensive_line_evaluation": {
            "avg_size": INFO_NA,
            "dominant_side": INFO_NA,
            "scheme_bias": INFO_NA
        },
        "skill_impact_review": {
            "top_threats": [],
            "yac_tendency": INFO_NA,
            "route_bias": INFO_NA
        },
        "formational_dna": {
            "base_sets": [],
            "red_zone_tendencies": INFO_NA,
            "disguise_rate": INFO_NA
        },
        "scoring_and_flow": {
            "points_per_quarter": INFO_NA,
            "game_script_vulnerability": INFO_NA,
            "red_zone_efficiency": INFO_NA
        },
        "situational_awareness": {
            "third_and_long": INFO_NA,
            "fourth_down": INFO_NA,
            "two_minute": INFO_NA
        },
        "psych_profile": {
            "penalty_rate": INFO_NA,
            "coach_style": INFO_NA,
            "bounce_back_rate": INFO_NA,
            "grit_score": INFO_NA
        },
        "tells_and_cues": {
            "pre_snap": [],
            "in_play": []
        },
        "practice_emphasis": {
            "defensive_line_focus": INFO_NA,
            "watch_list": [],
            "structural_gaps": INFO_NA
        }
    }
