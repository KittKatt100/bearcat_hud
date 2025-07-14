import streamlit as st
from memory.teams import team_memory

def main():
    st.set_page_config(page_title="Team Entry", page_icon="🏈", layout="centered")
    st.title("🏈 Bearcat HUD — Team Entry")

    # Input fields for school details
    st.subheader("Enter School Details")
    school = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State Abbreviation (e.g., GA, FL)")

    # Submit button
    if st.button("Search School"):
        if not school or not county or not state:
            st.warning("All fields are required.")
            return

        # Generate team key and load profile
        team_key = f"{school.strip().lower().replace(' ', '_')}_{county.strip().lower()}_{state.strip().upper()}"
        team_data = team_memory.load_team_profile(team_key)

        st.success(f"Profile found or created for: {school.title()} ({county.title()} County, {state.upper()})")

        # Display basic team info
        st.subheader("Team Information")
        st.text(f"📊 Record: {team_data.get('record', 'N/A')}")
        st.text(f"🐾 Mascot: {team_data.get('mascot', 'Not set')}")
        st.text(f"🎨 Colors: {', '.join(team_data.get('colors', [])) or 'Not set'}")

        # Show images if available
        if team_data.get("images"):
            st.subheader("Team Images")
            for img_url in team_data["images"]:
                st.image(img_url, width=300)
        else:
            st.info("No team images available.")

        # Future buttons could be added here for editing/updating profile
