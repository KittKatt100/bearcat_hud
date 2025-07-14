import streamlit as st
from core.bearcat_hud import BearcatHUD
from data import data_store
import pandas as pd
import os

hud = BearcatHUD()

st.title("🏈 Bearcat HUD: Tactical Scouting Interface")

st.sidebar.header("Opponent Setup")
school = st.sidebar.text_input("School", "Colquitt County")
county = st.sidebar.text_input("County", "Colquitt")
state = st.sidebar.text_input("State", "Georgia")

if st.sidebar.button("Set Opponent"):
    hud.set_opponent(school, county, state)
    data_store.save_opponent_data(school.replace(" ", "_"), hud.opponent)
    st.success(f"Opponent set to {school} ({county}, {state})")

st.subheader("📊 Scouting Module")
mod = st.selectbox("Choose a module", hud.list_modules())

if st.button("Run Module"):
    if hud.opponent:
        result = hud.run_module(mod)
        st.text_area("Module Report", result, height=200)
    else:
        st.warning("Set an opponent first.")

st.subheader("🎞️ Analyze Play Tells")
csv_file = st.file_uploader("Upload film CSV", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)
    st.write("Uploaded Film Data:", df)
    for _, row in df.iterrows():
        play = row.to_dict()
        tells = hud.identify_tells(play)
        if tells:
            st.markdown(f"**Play {row['play_id']}**: ")
            for t in tells:
                st.write("•", t)

st.subheader("🛠 Manual Play Entry")
with st.form("manual_play"):
    OL_pad = st.selectbox("OL Pad Level", ["", "low", "high"])
    QB_eyes = st.selectbox("QB Eyes", ["", "deep right", "middle", "left sideline"])
    motion = st.selectbox("Motion", ["", "fast jet", "none", "orbit"])
    align = st.selectbox("Alignment", ["", "tight split twins", "wide trips"])
    weight = st.selectbox("OL Weight", ["", "back-heavy", "forward-heavy"])
    submitted = st.form_submit_button("Analyze")

    if submitted:
        play = {
            "OL_pad_level": OL_pad,
            "QB_eyes": QB_eyes,
            "motion": motion,
            "alignment": align,
            "OL_weight_distribution": weight
        }
        tells = hud.identify_tells(play)
        if tells:
            st.success("Tells Found:")
            for t in tells:
                st.write("•", t)
        else:
            st.info("No strong tells detected.")
