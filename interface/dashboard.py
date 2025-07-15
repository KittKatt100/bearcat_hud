import streamlit as st
from modules.team_lookup import find_school

def set_theme():
    st.markdown("""
        <style>
        body {
            background-color: #1A0033;
            color: #FFD700;
        }
        .stApp {
            background-color: #1A0033;
        }
        .stTextInput>div>div>input {
            background-color: #2A0044;
            color: #FFD700;
        }
        .stFormSubmitButton>button {
            background-color: #FFD700;
            color: #1A0033;
        }
        .css-1d391kg, .css-10trblm, .stMarkdown {
            color: #FFD700 !important;
        }
        img {
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def display_value(label, value):
    if not value or "placeholder" in str(value).lower() or value.lower() in ["unknown", "n/a", "no data available"]:
        value = "Info Not Available"
    st.markdown(f"**{label}:** {value}")

def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")
    set_theme()

    st.image("https://pbs.twimg.com/profile_images/1062073323466227712/mQk4KnxY_400x400.jpg", width=100)
    st.title("💜💛 Bearcat HUD")
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

        if "error" in school_data:
            st.error(school_data["error"])
            return

        st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}")

        st.markdown(f"## {school_data.get('school', 'School')} - Overall Team Analysis")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                school_data.get("logo", "https://via.placeholder.com/150x150.png?text=Mascot"),
                caption="Mascot"
            )

        with col2:
            display_value("Mascot", school_data.get("mascot"))
            display_value("School Colors", school_data.get("colors"))
            display_value("City", school_data.get("city"))
            display_value("Classification", school_data.get("classification"))
            display_value("Record", school_data.get("record"))
            display_value("Region Standing", school_data.get("region_standing"))
            display_value("Recent Trends", school_data.get("recent_trends"))

        st.markdown("---")
        st.markdown("📊 *This is where your detailed Overall Team Analysis module will appear.*")

if __name__ == "__main__":
    main()
