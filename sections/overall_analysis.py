import os
import json
import streamlit as st
from datetime import datetime

ANALYSIS_TEXT = {
    "1. Opponent Identity": """School name, county, state, and relevant classification (e.g., GHSA 4A).
Current season record, region standings, and recent trends.""",
    "2. Offensive Philosophy Summary": """Run-pass ratio (RPO balance, ground vs. aerial bias).
Tempo and rhythm tendencies (e.g., huddle rate, no-huddle frequency).
Offensive coordinator background and play-calling style.
Use of motion, shifts, and tempo as tactical levers.""",
    "3. Quarterback Profile": """Physical tools, release speed, mobility under pressure.
Progression tendencies (reads left to right, single-read, or full progression).
Sack-to-scramble conversion rate.
Composure under duress and clutch efficiency (3rd/4th down behavior).""",
    "4. Offensive Line Evaluation": """Average size, height/weight differential across the line.
Dominant side (run or pass protection bias).
Pull/zone blocking frequency.
Double-team usage and combo block trends.""",
    "5. Skill Player Impact Review": """Top 3 offensive threats (RB, WR, TE).
Usage patterns: formation alignment, motion roles, and snap count involvement.
Broken tackle rate and yards after contact.
WR route tree tendencies (inside leverage vs. boundary threats).""",
    "6. Formational DNA": """Most-used formations by down and distance.
Frequency of tight vs. spread sets.
Red zone vs. field tendencies.
Formational disguise rate (how often formation is used to mask intent).""",
    "7. Scoring Patterns and Game Flow": """Points per quarter (start fast or finish strong?).
Game script vulnerability (do they fall behind early or dominate early?).
Red zone scoring percentage vs. field goals.
Two-point conversion behavior.""",
    "8. Situational Awareness": """3rd and long play tendencies.
4th down aggressiveness.
2-minute drill patterning.
End-of-half vs. end-of-game differential.""",
    "9. Psychological and Team Culture Profile": """Emotional volatility (penalty rate, post-turnover behavior).
Coaching style (aggressive, conservative, reactive).
Bounce-back rate after losses or turnovers.
Overall team grit score (subjective, based on tape and statistical comeback trends).""",
    "10. Tells and Tactical Cues": """Pre-snap indicators: stance depth, split width, motion triggers.
Offensive line “tells” in pass vs. run scenarios.
QB behavior under center vs. shotgun (eye scan, cadence variance).
RB alignment depth as an RPO or swing indicator."""
}

NOTES_PATH = "data/coach_notes"

def get_note_file(team_name):
    slug = team_name.lower().replace(" ", "_")
    return os.path.join(NOTES_PATH, f"{slug}_notes.json")

def load_notes(team_name):
    path = get_note_file(team_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_notes(team_name, notes):
    os.makedirs(NOTES_PATH, exist_ok=True)
    with open(get_note_file(team_name), "w") as f:
        json.dump(notes, f, indent=4)

def run_overall_analysis_ui(team_name):
    st.subheader("🧠 Overall Team Analysis")

    for section, content in ANALYSIS_TEXT.items():
        with st.expander(section, expanded=True):
            st.markdown(f"```\n{content}\n```")

    st.markdown("---")
    st.subheader("🗂️ Coach’s Notes & Strategic Additions")

    notes_data = load_notes(team_name)

    categories = [
        "D-Line Reads", "Red Zone Adjustments", "QB Cues",
        "Tempo Issues", "Formational Keys", "General Notes"
    ]

    category = st.selectbox("Select Note Category", categories)
    note = st.text_input("Enter your note and press Enter to save:")

    if note:
        today = datetime.today().strftime("%Y-%m-%d")
        if today not in notes_data:
            notes_data[today] = {}
        if category not in notes_data[today]:
            notes_data[today][category] = []
        notes_data[today][category].append(note)
        save_notes(team_name, notes_data)
        st.success("Note saved.")
        st.experimental_rerun()

    # Show saved notes
    if notes_data:
        st.markdown("### 📋 Saved Notes")
        for date in sorted(notes_data.keys(), reverse=True):
            st.markdown(f"#### 🗓️ {date}")
            for cat in notes_data[date]:
                st.markdown(f"**{cat}**")
                for i, line in enumerate(notes_data[date][cat]):
                    col1, col2 = st.columns([6, 1])
                    with col1:
                        edited = st.text_input(
                            f"{date}_{cat}_{i}", line, key=f"{date}_{cat}_{i}_edit"
                        )
                        if edited != line:
                            notes_data[date][cat][i] = edited
                            save_notes(team_name, notes_data)
                            st.success("Note updated.")
                            st.experimental_rerun()
                    with col2:
                        if st.button("🗑️", key=f"del_{date}_{cat}_{i}"):
                            del notes_data[date][cat][i]
                            if not notes_data[date][cat]:
                                del notes_data[date][cat]
                            if not notes_data[date]:
                                del notes_data[date]
                            save_notes(team_name, notes_data)
                            st.warning("Note deleted.")
                            st.experimental_rerun()
