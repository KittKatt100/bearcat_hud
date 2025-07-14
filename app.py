import streamlit as st
from core.team_lookup import find_school
from core.analysis_loader import load_team_analysis
from core.notes_handler import load_notes, save_note

st.set_page_config(page_title="Bearcat HUD", page_icon="🏈", layout="centered")

st.markdown("## 🏈 Bearcat HUD")
st.markdown("### Enter Opponent Team Info")

# Input fields
with st.form(key="school_form"):
    school_name = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State")
    submit_button = st.form_submit_button(label="Find School")

if submit_button and school_name and county and state:
    school = find_school(state, county, school_name)
    st.success(f"Found {school['school_name']} in {school['county']} County, {school['state'].upper()}")

    # School Info Display
    st.image(school.get("logo", ""), width=80, caption="Mascot")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Mascot:** {school.get('mascot', 'N/A')}")
        st.markdown(f"**City:** {school.get('city', 'N/A')}")
    with col2:
        st.markdown(f"**Classification:** {school.get('classification', 'N/A')}")
        st.markdown(f"**Record:** {school.get('record', 'N/A')}")
        st.markdown(f"**Region Standing:** {school.get('region_standing', 'N/A')}")

    # Divider before Analysis Section
    st.markdown("---")
    st.markdown(f"## Overall Analysis for {school['school_name']}")

    # Load and display full analysis
    analysis = load_team_analysis(school_name, county, state)
    for idx, section in enumerate(analysis.get("sections", []), start=1):
        st.markdown(f"### {idx}. {section['title']}")
        st.markdown(section['content'])

    # Coach Notes Section
    st.markdown("### 📝 Add Your Notes")
    note_input = st.text_area("Type your note here:", key="note_input")
    note_category = st.text_input("Save under category/date (e.g., 'Week 3 - Red Zone Reads')", key="note_category")
    if st.button("Save Note"):
        if note_input and note_category:
            save_note(school_name, county, state, note_category, note_input)
            st.success("Note saved.")
        else:
            st.warning("Both note and category are required to save.")

    # Display saved notes
    st.markdown("### 📚 Saved Notes")
    saved_notes = load_notes(school_name, county, state)
    for category, notes in saved_notes.items():
        st.markdown(f"**{category}**")
        for i, note in enumerate(notes, start=1):
            st.markdown(f"- {note}")
