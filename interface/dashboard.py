# bearcat_hud/interface/dashboard.py
import streamlit as st

# Use package‑relative imports (work when interface/ and core/ are inside bearcat_hud/)
try:
    from ..core.team_lookup import find_school
    from ..core.overall_analysis import render_overall_team_analysis
except ImportError:
    # fallback if you’re still finishing the move; harmless if not needed
    from core.team_lookup import find_school
    from core.overall_analysis import render_overall_team_analysis


def _header(title: str):
    st.markdown(
        f"""
        <h1 style="margin-top:.5rem;color:#F5C518;">{title}</h1>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")

    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:.6rem;">
          <span style="font-size:2rem;">🏈</span>
          <h1 style="margin:0;color:#F5C518;">Bearcat HUD</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("Enter Opponent Team Info")

    with st.form("team_form"):
        school = st.text_input("School Name")
        county = st.text_input("County")
        state = st.text_input("State")
        submitted = st.form_submit_button("Find School")

    if not submitted:
        return

    if not (school and county and state):
        st.error("Please fill in all three fields.")
        return

    data = find_school(state, county, school)
    st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}")

    _header(f"{school.title()} - Overall Team Analysis")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            data.get(
                "logo",
                "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg",
            ),
            caption="Mascot",
        )

    def show(label, value):
        v = value or "Info Not Available"
        if isinstance(v, str) and v.strip() == "":
            v = "Info Not Available"
        st.markdown(f"**{label}:** {v}")

    with col2:
        show("Mascot", data.get("mascot"))
        show("School Colors", data.get("colors"))
        show("City", data.get("city"))
        show("Classification", data.get("classification"))
        show("Record", data.get("record"))
        show("Region Standing", data.get("region_standing"))
        show("Recent Trends", data.get("recent_trends"))

    st.markdown("---")
    render_overall_team_analysis(data)
