import streamlit as st
from memory.teams.team_memory import load_team_profile, save_team_profile

def format_id(school, county, state):
    return f"{school.lower().replace(' ', '_')}__{county.lower()}__{state.lower()}"

def main():
    st.title("🏈 Dynamic Team Entry")

    # Step 1: Coach enters details
    school = st.text_input("School Name", placeholder="e.g. Bainbridge High School")
    county = st.text_input("County", placeholder="e.g. Decatur")
    state = st.text_input("State", placeholder="e.g. GA")

    if school and county and state:
        team_id = format_id(school, county, state)
        profile = load_team_profile(team_id)

        # Step 2: Load or show existing data
        st.subheader(f"📋 Profile: {school} ({county} County, {state})")

        profile["school"] = school
        profile["county"] = county
        profile["state"] = state
        profile["team_id"] = team_id

        profile["mascot"] = st.text_input("Mascot", value=profile.get("mascot", ""))
        profile["colors"] = {
            "primary": st.color_picker("Primary Color", value=profile.get("colors", {}).get("primary", "#000000")),
            "secondary": st.color_picker("Secondary Color", value=profile.get("colors", {}).get("secondary", "#ffffff"))
        }

        st.markdown("### 🖼️ Logo / Image URLs")
        urls = st.text_area("Image URLs (comma-separated)", value=", ".join(profile.get("images", [])))
        profile["images"] = [url.strip() for url in urls.split(",") if url.strip()]

        # Step 3: Show team preview
        st.markdown("### 🎨 Team Preview")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Mascot:** {profile.get('mascot', '')}")
            st.markdown(f"**Primary:** {profile['colors']['primary']}")
            st.markdown(f"**Secondary:** {profile['colors']['secondary']}")
        with col2:
            for img in profile.get("images", []):
                st.image(img, width=150)

        # Step 4: Save profile
        if st.button("💾 Save Team Profile"):
            save_team_profile(team_id, profile)
            st.success("Team profile saved successfully!")
