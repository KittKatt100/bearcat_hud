import streamlit as st
from interface import dashboard, team_profile

PAGES = {
    "Dashboard": dashboard,
    "Team Profiles": team_profile,
}

st.sidebar.title("📊 Bearcat HUD Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.main()  # ensure each module defines a main() function
