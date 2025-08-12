# interface/dashboard.py
import os
import streamlit as st

from core.team_lookup import find_school
from core.overall_analysis import build_overall_analysis
from core.analysis_loader import save_analysis, make_slug

PURPLE_BG = "#1b0f2d"   # very dark purple
GOLD_TEXT = "#ffd34d"   # gold

CUSTOM_CSS = f"""
<style>
  .stApp {{
      background-color: {PURPLE_BG};
  }}
  h1, h2, h3, h4, h5, h6, label, p, span {{
      color: {GOLD_TEXT} !important;
  }}
  .stTextInput>div>div>input, .stTextInput>div>div>textarea,
  .stSelectbox>div>div>div>input {{
      color: #eee !important;
      background-color: rgba(255,255,255,0.06) !important;
      border: 1px solid rgba(255,255,255,0.15);
  }}
  .found-box {{
      background: #14321f;
      border-radius: 8px;
      padding: 10px 14px;
      color: #d7ffd7;
      border: 1px solid #295c3a;
  }}
  .section-break {{
      border-top: 1px solid rgba(255,255,255,0.12);
      margin: 1.25rem 0;
  }}
</style>
"""

def _val(x):
    if not x or str(x).strip().lower() in {"unknown", "info not available", "n/a"}:
        return "Info Not Available"
    return x

def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.title("🏈 Bearcat HUD")

    st.subheader("Enter Opponent Team Info")
    with st.form("team_form", clear_on_submit=False):
        school = st.text_input("School Name")
        county = st.text_input("County")
        state  = st.text_input("State")
        submitted = st.form_submit_button("Find School")

    if not submitted:
        return

    if not (school and county and state):
        st.error("Please fill in all three fields.")
        return

    with st.spinner("Finding school and pulling quick intel..."):
        school_data = find_school(state, county, school)

    st.markdown(
        f'<div class="found-box">Found <b>{school.title()}</b> in {county.title()} County, {state.upper()}</div>',
        unsafe_allow_html=True
    )

    # Header
    st.markdown(f"## {school.title()} - Overall Team Analysis")

    # Logo + quick facts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            school_data.get("logo", "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"),
            caption="Mascot", use_column_width=True
        )
    with col2:
        st.markdown(f"**Mascot:** {_val(school_data.get('mascot'))}")
        st.markdown(f"**School Colors:** {_val(school_data.get('colors'))}")
        st.markdown(f"**City:** {_val(school_data.get('city'))}")
        st.markdown(f"**Classification:** {_val(school_data.get('classification'))}")
        st.markdown(f"**Record:** {_val(school_data.get('record'))}")
        st.markdown(f"**Region Standing:** {_val(school_data.get('region_standing'))}")
        st.markdown(f"**Recent Trends:** {_val(school_data.get('recent_trends'))}")

    st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

    # Build and save analysis
    with st.spinner("Generating Overall Team Analysis…"):
        analysis = build_overall_analysis(school_data)

    slug = make_slug(school, county, state)
    path = save_analysis(slug, analysis)

    st.markdown("### Analysis Summary")
    st.json(analysis)

    st.caption(f"Saved analysis to: `{path}`")
