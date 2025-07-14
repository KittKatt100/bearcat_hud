import streamlit as st
from bearcat_hud.core.bearcat_hud import BearcatHUD

# Page configuration
st.set_page_config(page_title="Bearcat HUD", layout="wide")

# Title
st.title("Bearcat HUD Dashboard")

# Initialize BearcatHUD
hud = BearcatHUD()

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Load Game Data")
    uploaded_file = st.file_uploader("Upload Game CSV", type=["csv"])
    if uploaded_file:
        hud.load_data(uploaded_file)
        st.success("Data loaded successfully!")

with col2:
    if hud.data is not None:
        st.header("Dashboard View")
        st.dataframe(hud.data.head())
    else:
        st.info("Upload a game CSV to begin.")

