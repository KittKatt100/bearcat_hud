import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        .info-not-available {
            color: #AAAAAA;
            font-style: italic;
        }
        </style>
    """, unsafe_allow_html=True)

def display_value(label, value):
    if not value or "placeholder" in str(value).lower() or \
        value.lower() in ["unknown", "n/a", "no data available"]:
        st.markdown(f"**{label}:** <span class='info-not-available'>Info Not Available</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"**{label}:** {value}")

def generate_overall_analysis(school_data):
    """
    Generates a placeholder for the Overall Team Analysis.
    Replace/mock these with actual logic as you collect more opponent data!
    """
    school_name = school_data.get('school', 'The Team').title()

    return f"""
    <h4>Overview for {school_name}</h4>
    <p>This is a demonstration of what the "Overall Team Analysis" will look like.</p>

    <h3>Strengths 💪</h3>
    <ul>
        <li>Strong running game behind a physical offensive line</li>
        <li>Aggressive linebacker play, especially on early downs</li>
        <li>Special teams consistently pin opponents deep</li>
    </ul>

    <h3>Weaknesses 📉</h3>
    <ul>
        <li>Pass defense struggles with deep routes</li>
        <li>Quarterback can be forced into mistakes under blitz pressure</li>
        <li>Secondary tackling can be inconsistent in open space</li>
    </ul>

    <h3>Key Players to Watch 👀</h3>
    <ul>
        <li>#7 - Dual-threat QB with a strong arm and quick feet</li>
        <li>#22 - RB who excels at yards after contact</li>
        <li>#55 - Defensive end, leads the team in sacks</li>
    </ul>

    <h3>Recent Trends 📈</h3>
    <ul>
        <li>Won 3 of last 4 games, all by less than one touchdown</li>
        <li>Averaging 150+ rushing yards/game in last month</li>
        <li>Turnover margin: -2 over their last 5 games</li>
    </ul>

    <p><i>This is sample analysis; replace with live scouting and stat breakdowns as you build your workflow!</i></p>
    """

def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")
    set_theme()

    st.image("https://pbs.twimg.com/profile_images/1062073323466227712/mQk4KnxY_400x400.jpg", width=100)
    st.title("💜💛 Bearcat HUD")
    st.subheader("Enter Opponent Team Info")

    with st.form("team_form"):
        # You can leave empty or use these default values for faster testing
        school = st.text_input("School Name", value="Port St. Joe High")
        county = st.text_input("County", value="Gulf")
        state = st.text_input("State", value="Florida")
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
        st.markdown("## 🧠 Overall Team Analysis")
        st.markdown(generate_overall_analysis(school_data), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
