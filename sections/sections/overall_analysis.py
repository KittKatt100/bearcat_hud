import os
import json
import streamlit as st

ANALYSIS_PATH = "data/analysis"

def get_analysis_filepath(team_name):
    filename = f"{team_name.lower().replace(' ', '_')}_analysis.json"
    return os.path.join(ANALYSIS_PATH, filename)

def load_analysis(team_name):
    path = get_analysis_filepath(team_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_analysis(team_name, data):
    os.makedirs(ANALYSIS_PATH, exist_ok=True)
    path = get_analysis_filepath(team_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def run_overall_analysis_ui(team_name):
    st.subheader("🧠 Overall Team Analysis")

    data = load_analysis(team_name)

    with st.form(f"analysis_form_{team_name}"):
        opponent_identity = st.text_area("1. Opponent Identity", data.get("opponent_identity", ""))
        offensive_philosophy = st.text_area("2. Offensive Philosophy Summary", data.get("offensive_philosophy", ""))
        quarterback_profile = st.text_area("3. Quarterback Profile", data.get("quarterback_profile", ""))
        offensive_line = st.text_area("4. Offensive Line Evaluation", data.get("offensive_line", ""))
        skill_review = st.text_area("5. Skill Player Impact Review", data.get("skill_review", ""))
        formational_dna = st.text_area("6. Formational DNA", data.get("formational_dna", ""))
        scoring_patterns = st.text_area("7. Scoring Patterns and Game Flow", data.get("scoring_patterns", ""))
        situational_awareness = st.text_area("8. Situational Awareness", data.get("situational_awareness", ""))
        psychological = st.text_area("9. Psychological and Team Culture Profile", data.get("psychological", ""))
        tells_cues = st.text_area("10. Tells and Tactical Cues", data.get("tells_cues", ""))

        submitted = st.form_submit_button("💾 Save Analysis")
        if submitted:
            updated = {
                "opponent_identity": opponent_identity,
                "offensive_philosophy": offensive_philosophy,
                "quarterback_profile": quarterback_profile,
                "offensive_line": offensive_line,
                "skill_review": skill_review,
                "formational_dna": formational_dna,
                "scoring_patterns": scoring_patterns,
                "situational_awareness": situational_awareness,
                "psychological": psychological,
                "tells_cues": tells_cues,
            }
            save_analysis(team_name, updated)
            st.success(f"✔️ Analysis for {team_name} saved successfully.")
