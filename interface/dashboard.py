import streamlit as st
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.bearcat_hud import BearcatHUD

st.set_page_config(page_title="Bearcat HUD", layout="wide")
st.title("🏈 Bearcat HUD")

# Initialize the HUD object
try:
    hud = BearcatHUD()
except Exception as e:
    st.error(f"❌ Failed to initialize HUD: {e}")
    st.stop()

# Debug: Show available games
if not hasattr(hud, "get_game_list"):
    st.error("❌ BearcatHUD does not have method 'get_game_list'")
    st.stop()

st.sidebar.header("Select Options")

game_list = hud.get_game_list()
if not game_list:
    st.warning("⚠️ No games found.")
    st.stop()

selected_game = st.sidebar.selectbox("Choose a game", game_list)

quarter_list = hud.get_quarters(selected_game)
if not quarter_list:
    st.warning("⚠️ No quarters found for selected game.")
    st.stop()

selected_quarter = st.sidebar.selectbox("Choose a quarter", quarter_list)

st.header(f"Plays for {selected_game} – Quarter {selected_quarter}")
plays = hud.get_plays(selected_game, selected_quarter)
st.dataframe(plays)
