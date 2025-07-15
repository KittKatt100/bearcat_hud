import streamlit as st
from modules.team_lookup import find_school  # Confirm this is the correct path

st.set_page_config(page_title="Bearcat HUD", layout="centered")

def main():
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

        if school_data:
            st.success(f"{school.title()} found in {county.title()} County, {state.upper()}")

            st.markdown(f"## {school_data.get('school_name', school.title())}")

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
                display_value("Classification", school_data.get('classification'))
                display_value("City", school_data.get('city'))
                display_value("Record", school_data.get('record'))
                display_value("Region Standing", school_data.get('region_standing'))
                display_value("Recent Trends", school_data.get('recent_trends'))

            # Placeholder for the full Overall Team Analysis section (expansion not yet animated)
            st.markdown("---")
            st.subheader("🧠 Overall Team Analysis")
            st.info("Detailed analysis will appear here once implemented.")

        else:
            st.error("No data found for that school. Please try again.")

if __name__ == "__main__":
    main()
