import streamlit as st
import datetime
import os
import json

from core.team_lookup import find_school
from core.analysis_generator import generate_team_analysis
from core.coach_notes import save_note, load_notes

st.set_page_config(page_title="Bearcat HUD", layout="wide")

st.markdown(
    """
    <style>
        .scroll-target {
            padding-top: 100px;
        }
        .school-header {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 50px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("## 🏈 Bearcat HUD")
st.markdown("### Enter Opponent Team Info")

school_name = st.text_input("School Name")
county = st.text_input("County")
state = st.text_input("State")

if st.button("Find School"):
    school_data = find_school(state, county, school_name)
    
    st.success(f"Found {school_data['school_name']} in {school_data['county']} County, {school_data['state'].upper()}")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(school_data["logo"], caption="Mascot", width=100)
    with col2:
        st.markdown(f"**Mascot:** {school_data['mascot']}")
        st.markdown(f"**School Colors:** {school_data['colors']}")
        st.markdown(f"**City:** {school_data['city']}")

    # Scroll to analysis
    st.markdown(
        f"""
        <script>
            window.scrollTo({{top: document.body.scrollHeight, behavior: 'smooth'}});
        </script>
        """,
        unsafe_allow_html=True
    )

    # Header with School Name
    st.markdown(f"""<div class="school-header">{school_data['school_name']} - Overall Team Analysis</div>""", unsafe_allow_html=True)

    st.markdown("---")
    analysis = generate_team_analysis(school_data)
    st.markdown(analysis)

    st.markdown("### 📝 Coach Notes")

    today = datetime.date.today().isoformat()
    notes = load_notes(school_data["school_name"], today)
    if notes:
        for i, entry in enumerate(notes):
            edited = st.text_area(f"Note {i+1}", entry, key=f"edit_note_{i}")
            if edited != entry:
                notes[i] = edited
                save_note(school_data["school_name"], today, edited, overwrite_index=i)

    new_note = st.text_area("Add New Note", "")
    if st.button("Save Note"):
        if new_note.strip():
            save_note(school_data["school_name"], today, new_note.strip())
            st.experimental_rerun()
