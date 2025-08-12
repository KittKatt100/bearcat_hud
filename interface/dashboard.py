# interface/dashboard.py
import streamlit as st
from core.team_lookup import find_school

INFO_NA = "Info Not Available"

def _val(v):
    if not v or str(v).strip().lower() in {"unknown", "n/a", "no data available", "placeholder"}:
        return INFO_NA
    return v

def main():
    st.markdown(
        """
        <style>
            .bearcat-bg {background-color:#140422; padding:8px 14px; border-radius:8px;}
            .bearcat-h1 {color:#f7d23e; font-weight:800; font-size:2.2rem;}
            .bearcat-label {color:#ddd;}
            .stButton>button {background:#f7d23e; color:#140422; font-weight:700;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="bearcat-bg"><span class="bearcat-h1">🏈 Bearcat HUD</span></div>', unsafe_allow_html=True)
    st.subheader("Enter Opponent Team Info")

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

    st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}")

    st.markdown(f"## {school.title()} - Overall Team Analysis")

    col1, col2 = st.columns([1,2], gap="large")
    with col1:
        st.image(
            data.get("logo", "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"),
            caption="Mascot",
        )

    def row(label, key):
        st.markdown(f"**{label}:** {_val(data.get(key))}")

    with col2:
        row("Mascot", "mascot")
        row("School Colors", "colors")
        row("City", "city")
        row("Classification", "classification")
        row("Record", "record")
        row("Region Standing", "region_standing")
        row("Recent Trends", "recent_trends")

    st.markdown("---")
    st.info("📊 This is where your detailed Overall Team Analysis module will appear.")

if __name__ == "__main__":
    main()
