import streamlit as st
from core.team_lookup import find_school
from core.analysis_loader import load_overall_analysis
from core.notes_handler import load_notes, save_note
from datetime import datetime

st.set_page_config(page_title="Bearcat HUD", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏈 Bearcat HUD</h1>", unsafe_allow_html=True)

# Step 1 – Input Form
st.subheader("Enter Opponent Team Info")
with st.form("team_info_form"):
    school_name = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State")
    submitted = st.form_submit_button("Find School")

# Step 2 – School Info & Analysis
if submitted and school_name and county and state:
    school = find_school(state, county, school_name)
    st.success(f"{school['school_name']} found in {school['county']} County, {school['state']}")

    # Header and Metadata
    st.markdown(f"## {school['school_name']} Overall Team Analysis")
    cols = st.columns([1, 3])
    with cols[0]:
        st.image(school["logo"], width=150, caption="Mascot")
    with cols[1]:
        st.markdown(f"**Mascot:** {school['mascot']}")
        st.markdown(f"**School Colors:** {school['colors']}")
        st.markdown(f"**City:** {school['city']}")
        st.markdown(f"**Classification:** {school['classification']}")
        st.markdown(f"**Record:** {school['record']}")
        st.markdown(f"**Region Standing:** {school['region_standing']}")
        st.markdown(f"**Recent Trends:** {school['recent_trends']}")

    # Step 3 – Full Analysis
    st.markdown("---")
    st.markdown("### 📊 Strategic Overview")
    analysis = load_overall_analysis(school['school_name'], school['county'], school['state'])
    for section, content in analysis.items():
        st.markdown(f"#### {section}")
        st.markdown(content)

    # Step 4 – Notes Section
    st.markdown("---")
    st.markdown("### 📝 Coach's Notes")

    today = datetime.now().strftime("%Y-%m-%d")
    category = st.text_input("Enter Note Category", value=today)

    existing_notes = load_notes(school['school_name'], category)
    edited_notes = st.text_area("Edit Existing Notes", value=existing_notes, height=200)

    new_note = st.text_input("Add New Note")

    if st.button("Save Note"):
        combined = edited_notes.strip()
        if new_note.strip():
            combined += "\n" + new_note.strip()
        save_note(school['school_name'], category, combined)
        st.success("Note saved successfully.")
