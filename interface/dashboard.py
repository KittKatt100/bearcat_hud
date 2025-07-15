import streamlit as st

def main():
    st.set_page_config(page_title="Bearcat HUD", layout="centered")

    st.title("🏈 Bearcat HUD")
    st.subheader("Enter Opponent Team Info")

    with st.form("team_form"):
        school = st.text_input("School Name")
        county = st.text_input("County")
        state = st.text_input("State")
        submitted = st.form_submit_button("Find School")

    if submitted:
        if not (school and county and state):
            st.error("Please fill in all three fields.")
            return

        st.success(f"Found {school.title()} in {county.title()} County, {state.upper()}")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image("https://via.placeholder.com/150x150.png?text=Mascot", caption="Mascot")

        with col2:
            st.markdown("**Mascot:** Tigers (placeholder)")
            st.markdown("**School Colors:** Blue & Gold (placeholder)")
            st.markdown("**City:** Sampletown (placeholder)")

if __name__ == "__main__":
    main()
