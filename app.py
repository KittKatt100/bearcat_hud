import streamlit as st
from interface import dashboard

def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")
    dashboard.main()

if __name__ == "__main__":
    main()
