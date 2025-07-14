import streamlit as st
from core.team_lookup import find_school
from core.overall_analysis import load_overall_analysis

st.set_page_config(page_title="Bearcat HUD", layout="wide")

st.title("🏈 Bearcat HUD")
st.header("Enter Opponent Team Info")

with st.form("school_entry"):
    school_name = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State")

    submitted = st.form_submit_button("Find School")

if submitted:
    school_info = find_school(state, county, school_name)

    st.success(f"Found {school_info['school_name']} in {school_info['county']} County, {school_info['state'].upper()}")
    st.image(school_info.get("logo", ""), width=80, caption="Mascot")
    st.markdown(f"**Mascot:** {school_info.get('mascot', 'N/A')}")
    st.markdown(f"**School Colors:** {school_info.get('colors', 'N/A')}")
    st.markdown(f"**City:** {school_info.get('city', 'N/A')}")

    st.divider()
    st.subheader("📊 Overall Team Analysis")

    analysis = load_overall_analysis(school_name, county, state)

    with st.expander("1. Opponent Identity", expanded=True):
        st.json(analysis.get("identity", {}))

    with st.expander("2. Offensive Philosophy Summary"):
        st.json(analysis.get("offense", {}))

    with st.expander("3. Quarterback Profile"):
        st.json(analysis.get("quarterback", {}))

    with st.expander("4. Offensive Line Evaluation"):
        st.json(analysis.get("oline", {}))

    with st.expander("5. Skill Player Impact Review"):
        st.json(analysis.get("skill", {}))

    with st.expander("6. Formational DNA"):
        st.json(analysis.get("formation", {}))

    with st.expander("7. Scoring Patterns and Game Flow"):
        st.json(analysis.get("scoring", {}))

    with st.expander("8. Situational Awareness"):
        st.json(analysis.get("situational", {}))

    with st.expander("9. Psychological and Team Culture Profile"):
        st.json(analysis.get("psych", {}))

    with st.expander("10. Tells and Tactical Cues"):
        st.json(analysis.get("tells", {}))
