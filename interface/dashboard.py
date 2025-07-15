import streamlit as st
from core.team_lookup import find_school  # ✅ Correct import path

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

        school_data = find_school(state, county, school)
        st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                school_data.get("logo", "https://via.placeholder.com/150x150.png?text=Mascot"),
                caption="Mascot"
            )

        def display_value(label, value):
            if not value or "placeholder" in str(value).lower() or value.lower() in ["unknown", "n/a", "no data available"]:
                value = "Info Not Available"
            st.markdown(f"**{label}:** {value}")

        with col2:
            display_value("Mascot", school_data.get('mascot'))
            display_value("School Colors", school_data.get('colors'))
            display_value("City", school_data.get('city'))
            display_value("Classification", school_data.get('classification'))
            display_value("Record", school_data.get('record'))
            display_value("Region Standing", school_data.get('region_standing'))
            display_value("Recent Trends", school_data.get('recent_trends'))

if __name__ == "__main__":
    main()
