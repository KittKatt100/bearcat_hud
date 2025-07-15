import streamlit as st
from core.web_lookup import get_school_web_data  # Adjust the import path as needed

def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")

    st.title("🏈 Bearcat HUD")
    st.subheader("Enter Opponent Team Info")

    with st.form("team_form"):
        school = st.text_input("School Name")
        county = st.text_input("County")
        state = st.text_input("State")
        submitted = st.form_submit_button("Find School")

    if submitted:
        if not (school and county and state):
            st.error("Please fill in all three fields.")
            return

        # Fetch real data using DuckDuckGo (or your own lookup function)
        school_data = get_school_web_data(school, county, state)

        st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                school_data.get("logo", "https://via.placeholder.com/150x150.png?text=Mascot"),
                caption="Mascot"
            )

        with col2:
            st.markdown(f"**Mascot:** {school_data.get('mascot', 'Unknown')}")
            st.markdown(f"**School Colors:** {school_data.get('colors', 'Unknown')}")
            st.markdown(f"**City:** {school_data.get('city', 'Unknown')}")
            st.markdown(f"**Classification:** {school_data.get('classification', 'Unknown')}")
            st.markdown(f"**Record:** {school_data.get('record', 'Unknown')}")
            st.markdown(f"**Region Standing:** {school_data.get('region_standing', 'Unknown')}")
            st.markdown(f"**Recent Trends:** {school_data.get('recent_trends', 'Unknown')}")

if __name__ == "__main__":
    main()
