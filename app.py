import streamlit as st
from bearcat_hud.memory.team_memory import load_team_profile, save_team_profile
from bearcat_hud.metadata.team_lookup import find_school
from bearcat_hud.sections.overall_analysis import run_overall_analysis_ui

st.set_page_config(page_title="Bearcat HUD", page_icon="🏈", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏈 Bearcat HUD</h1>", unsafe_allow_html=True)
st.markdown("## Enter Opponent Team Info")

# Input fields
with st.form("team_form"):
    school_name = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State")
    submit = st.form_submit_button("Find School")

if submit:
    team_data = find_school(state, county, school_name)

    if team_data:
        st.success(f"Found {team_data['school_name']} in {team_data['county']} County, {team_data['state'].upper()}")

        col1, col2 = st.columns([1, 3])

        with col1:
            st.image(team_data.get("logo"), width=90, caption="Mascot")

        with col2:
            st.markdown(f"**Mascot:** {team_data.get('mascot')} (placeholder)")
            st.markdown(f"**School Colors:** {team_data.get('colors')} (placeholder)")
            st.markdown(f"**City:** {team_data.get('city')} (placeholder)")

        # Save team profile to memory
        save_team_profile(team_data["school_name"], team_data)

        # Show the overall analysis module
        run_overall_analysis_ui(team_data["school_name"])

    else:
        st.error("School not found. Please check the spelling or try again.")
