import streamlit as st
from core.team_lookup import find_school
from core.analysis_loader import load_team_analysis
from core.notes_handler import save_note, load_notes

st.set_page_config(page_title="Bearcat HUD", layout="wide")
st.markdown("<h1 style='text-align: center;'>🏈 Bearcat HUD</h1>", unsafe_allow_html=True)
st.markdown("## Enter Opponent Team Info")

school_name = st.text_input("School Name")
county = st.text_input("County")
state = st.text_input("State")

if st.button("Find School"):
    team_info = find_school(state, county, school_name)
    if team_info:
        st.success(f"Found {team_info['school_name']} in {team_info['county']} County, {team_info['state'].upper()}")

        # Show basic info
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(team_info.get("logo", ""), width=80, caption="Mascot")
        with col2:
            st.markdown(f"**Mascot:** {team_info.get('mascot', 'N/A')}")
            st.markdown(f"**School Colors:** {team_info.get('colors', 'N/A')}")
            st.markdown(f"**City:** {team_info.get('city', 'N/A')}")

        # Header + Full Analysis
        st.markdown("---")
        st.markdown(f"## Overall Team Analysis: {team_info['school_name']}")
        st.markdown("This section auto-loads the opponent’s full offensive and psychological profile.")
        analysis = load_team_analysis(school_name, county, state)

        for section, content in analysis.items():
            st.markdown(f"### {section}")
            if isinstance(content, dict):
                for key, value in content.items():
                    st.markdown(f"- **{key}**: {value}")
            elif isinstance(content, list):
                for item in content:
                    st.markdown(f"- {item}")
            else:
                st.markdown(f"- {content}")

        st.markdown("---")
        st.markdown("## 📝 Add Coaching Notes")

        existing_notes = load_notes(school_name, county, state)
        for note in existing_notes:
            with st.expander(f"{note['category']} – {note['timestamp']}"):
                edited = st.text_area("Edit Note", note['content'], key=f"note_{note['timestamp']}")
                if edited != note['content']:
                    note['content'] = edited
                    save_note(school_name, county, state, note['category'], edited, timestamp=note['timestamp'])

        st.markdown("### ➕ Add New Note")
        category = st.text_input("Category")
        new_note = st.text_area("New Note", placeholder="Type coaching note and hit Enter...")
        if st.button("Save Note"):
            save_note(school_name, county, state, category, new_note)
            st.experimental_rerun()
    else:
        st.error("School not found.")
