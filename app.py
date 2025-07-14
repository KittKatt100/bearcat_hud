import streamlit as st
from interface.dashboard import render_dashboard

def main():
    st.set_page_config(page_title="Bearcat HUD", page_icon="🏈", layout="wide")
    render_dashboard()

if __name__ == "__main__":
    main()

