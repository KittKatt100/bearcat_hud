import streamlit as st
from interface import dashboard, team_entry

PAGES = {
    "Team Entry": team_entry,
    "Game Dashboard": dashboard
}

def main():
    st.set_page_config(page_title="Bearcat HUD", page_icon="🏈", layout="wide")

    st.sidebar.title("Select Options")
    default_index = list(PAGES.keys()).index("Team Entry")  # Make Team Entry default
    page = st.sidebar.radio("Navigate", list(PAGES.keys()), index=default_index)

    PAGES[page].main()

if __name__ == "__main__":
    main()
