import streamlit as st
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.bearcat_hud import BearcatHUD

st.set_page_config(page_title="Bearcat HUD", layout="wide")

st.title("🏈 Bearcat HUD")

hud = BearcatHUD()

st.sidebar.header("Select Options")
selected_game = st.sidebar.selectbox("Choose a game", hud.get_game_list())
selected_quarter = st.sidebar.selectbox("Choose a quarter", hud.get_quarter_list(selected_game))

st.header(f"Plays for {selected_game} - Quarter {selected_quarter}")
plays = hud.get_plays(selected_game, selected_quarter)
st.dataframe(plays)
