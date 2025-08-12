# bearcat_hud/interface/dashboard.py
import streamlit as st
from bearcat_hud.core.team_lookup import find_school  # ✅ correct import

def _value(v: str) -> str:
    if not v or str(v).strip().lower() in {"unknown", "n/a", "info not available"}:
        return "Info Not Available"
    return str(v)

def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")

    # Bainbridge theme styling
    st.markdown("""
        <style>
        .stApp { background-color: #1b0d27; }                 /* very dark purple */
        .bearcat-title { color: #ffd54f; font-size: 2.4rem; font-weight: 800; }
        .section-title { color: #ffd54f; font-size: 1.6rem; font-weight: 700; margin-top: 1rem; }
        .label { color: #ffd54f; font-weight: 700; }
        .val { color: #ffffff; }
        .note { color: #ffd54f; opacity: .85; }
        .stButton>button { background:#ffd54f; color:#1b0d27; font-weight:700; border:0; }
        .stTextInput>div>div>input { background:#2a153b; color:#fff; }
        .stAlert { background:#103a22 !important; }           /* confirmation bar */
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bearcat-title">🏈 Bearcat HUD</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Enter Opponent Team Info</div>', unsafe_allow_html=True)

    with st.form("team_form"):
        school = st.text_input("School Name")
        county = st.text_input("County")
        state  = st.text_input("State")
        submitted = st.form_submit_button("Find School")

    if not submitted:
        return

    if not (school and county and state):
        st.error("Please fill in all three fields.")
        return

    data = find_school(state=state, county=county, school_name=school)

    st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}.")

    st.markdown(
        f'<div class="section-title">{school.title()} - Overall Team Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            data.get("logo") or "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
            caption="Mascot"
        )

    with col2:
        st.markdown(f'<span class="label">Mascot:</span> <span class="val">{_value(data.get("mascot"))}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="label">School Colors:</span> <span class="val">{_value(data.get("colors"))}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="label">City:</span> <span class="val">{_value(data.get("city"))}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="label">Classification:</span> <span class="val">{_value(data.get("classification"))}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="label">Record:</span> <span class="val">{_value(data.get("record"))}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="label">Region Standing:</span> <span class="val">{_value(data.get("region_standing"))}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="label">Recent Trends:</span> <span class="val">{_value(data.get("recent_trends"))}</span>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<span class="note">📊 This is where your detailed Overall Team Analysis module will appear.</span>', unsafe_allow_html=True)
