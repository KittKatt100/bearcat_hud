import streamlit as st
from core import team_memory

st.title("🏈 Team Memory Manager")

# Sidebar: Choose or enter a team
team_name = st.text_input("Enter team name", placeholder="e.g. Bainbridge Bearcats")

if team_name:
    profile = team_memory.load_team_profile(team_name)

    st.subheader(f"📋 Team Profile: {team_name}")
    profile["record"] = st.text_input("Team Record (e.g. 8-2)", value=profile.get("record", ""))

    st.markdown("### 🔥 Top Plays")
    top_plays = st.text_area("Enter top plays (comma-separated)", 
                             value=", ".join(profile.get("top_plays", [])))
    profile["top_plays"] = [play.strip() for play in top_plays.split(",") if play.strip()]

    st.markdown("### ❌ Weaknesses")
    weaknesses = st.text_area("Enter known weaknesses (comma-separated)",
                               value=", ".join(profile.get("weaknesses", [])))
    profile["weaknesses"] = [w.strip() for w in weaknesses.split(",") if w.strip()]

    st.markdown("### 📊 Avg Yards by Quarter")
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    for q in quarters:
        default_val = profile.get("avg_quarter_yards", {}).get(q, 0)
        val = st.number_input(f"{q} Avg Yards", min_value=0, value=default_val, step=1)
        profile.setdefault("avg_quarter_yards", {})[q] = val

    st.markdown("### 📐 Formation Notes")
    formation_keys = list(profile.get("formations", {}).keys()) or ["I-Form", "Shotgun", "Wildcat"]
    for fk in formation_keys:
        val = st.text_area(f"Notes for {fk}", value=profile.get("formations", {}).get(fk, ""))
        profile.setdefault("formations", {})[fk] = val

    if st.button("💾 Save Team Profile"):
        team_memory.save_team_profile(team_name, profile)
        st.success("Team profile saved!")

def main():
    st.title("🏈 Team Memory Manager")

