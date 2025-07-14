import streamlit as st
from modules import team_lookup

st.set_page_config(page_title="Bearcat HUD", layout="wide")

# ---- HEADER ----
st.markdown("<h1 style='text-align: center;'>🏈 Bearcat HUD</h1>", unsafe_allow_html=True)
st.subheader("Enter Opponent Team Info")

# ---- TEAM ENTRY FORM ----
with st.form("team_form"):
    school_name = st.text_input("School Name")
    county = st.text_input("County")
    state = st.text_input("State")
    submit = st.form_submit_button("Find School")

# ---- LOOKUP AND DISPLAY RESULTS ----
if submit:
    result = team_lookup.find_school(state, county, school_name)
    
    if result:
        st.success(f"Found {school_name} in {county} County, {state.upper()}")
        col1, col2 = st.columns([1, 3])

        with col1:
            if "logo" in result and result["logo"]:
                st.image(result["logo"], width=100, caption="Mascot")
            else:
                st.warning("Mascot image not available.")

        with col2:
            st.markdown(f"**Mascot:** {result.get('mascot', 'N/A')}")
            st.markdown(f"**School Colors:** {result.get('colors', 'N/A')}")
            st.markdown(f"**City:** {result.get('city', 'N/A')}")
    else:
        st.error("School not found. Please check spelling or try another combination.")
