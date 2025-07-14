import streamlit as st

def main():
    st.title("Bearcat HUD")

    st.header("Enter Team Information")

    school = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State")

    if school and county and state:
        st.success(f"Searching for: {school}, {county} County, {state}")
        # Placeholder for mascot, colors, and images
        st.image("https://via.placeholder.com/300x100.png?text=School+Mascot", caption="Mascot (Placeholder)")
        st.markdown("**Colors:** Blue & Gold (Placeholder)")
    else:
        st.info("Please enter all fields above to retrieve school information.")
