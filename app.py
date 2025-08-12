# app.py
import streamlit as st
from interface.dashboard import main as dashboard_main

st.set_page_config(page_title="Bearcat HUD", layout="centered")
dashboard_main()
