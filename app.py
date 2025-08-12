# app.py
import streamlit as st
from interface.dashboard import main

if __name__ == "__main__":
    st.set_page_config(page_title="Bearcat HUD", layout="centered")
    main()
