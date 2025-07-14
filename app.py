import streamlit as st
from interface import dashboard, team_entry

PAGES = {
    "Dashboard": dashboard,
    "Team Entry": team_entry
}

st.sidebar.title("📊 Bearcat HUD")
page = st.sidebar.radio("Navigate", list(PAGES.keys()))
PAGES[page].main()
