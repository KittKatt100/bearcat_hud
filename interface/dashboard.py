import streamlit as st
import sys
import os

# Ensure the project root is in the Python path
# This is crucial for relative imports to work correctly
# /mount/src/bearcat-hud
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now, import modules using their paths relative to the project root
from core.team_lookup import find_school
from sections.overall_analysis import run_overall_analysis_ui
from modules.ol_scheme import analyze_ol
from modules.quarterback_targeting import analyze_qb
from core.web_lookup import get_school_web_data

st.set_page_config(page_title="Bearcat HUD", layout="wide")

# --- UI Styling (as requested in Next Steps) ---
st.markdown("""
    <style>
    .reportview-container {
        background: #280230; /* Dark Purple */
    }
    .main .block-container {
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700; /* Gold */
        text-align: center;
    }
    .stTextInput label, .stSelectbox label, .stTextArea label, .stNumberInput label {
        color: #FFD700; /* Gold */
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea, .stNumberInput>div>input {
        background-color: #4F006D; /* Slightly lighter purple */
        color: white;
    }
    .stButton>button {
        background-color: #FFD700; /* Gold */
        color: #280230; /* Dark Purple */
        font-weight: bold;
    }
    .stSuccess {
        background-color: #4CAF50; /* Green */
        color: white;
    }
    .stWarning {
        background-color: #FFA500; /* Orange */
        color: white;
    }
    /* Center content (adjust as needed) */
    .css-1d391kg {
        justify-content: center;
    }
    .css-h5f0s3 { /* Adjust this class if centering doesn't apply to main block */
        max-width: 800px; /* Example max width */
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)
# --- End UI Styling ---

st.markdown("<h1 style='text-align: center;'>🏈 Bearcat HUD</h1>", unsafe_allow_html=True)

# Step 1 – Input Form
st.subheader("Enter Opponent Team Info")
with st.form("team_info_form"):
    school_name = st.text_input("School Name", key="dashboard_school_name")
    county = st.text_input("County", key="dashboard_county")
    state = st.text_input("State Abbreviation (e.g., FL, GA)", key="dashboard_state")
    submitted = st.form_submit_button("Find School")

# Step 2 – School Info & Analysis
if submitted and school_name and county and state:
    school_info = get_school_web_data(school_name, county, state)

    st.success(f"Profile found or created for: {school_info['school_name']} ({school_info['county']} County, {school_info['state']})")

    # Header and Metadata
    st.markdown(f"## {school_info['school_name']} Overall Team Analysis")
    cols = st.columns([1, 3])
    with cols[0]:
        st.image(school_info.get("logo", "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"), width=150, caption="Mascot")
    with cols[1]:
        st.markdown(f"**Mascot:** {school_info.get('mascot', 'Info Not Available')}")
        st.markdown(f"**School Colors:** {school_info.get('colors', 'Info Not Available')}")
        st.markdown(f"**City:** {school_info.get('city', 'Info Not Available')}")
        st.markdown(f"**Classification:** {school_info.get('classification', 'Info Not Available')}")
        st.markdown(f"**Record:** {school_info.get('record', 'Info Not Available')}")
        st.markdown(f"**Region Standing:** {school_info.get('region_standing', 'Info Not Available')}")
        st.markdown(f"**Recent Trends:** {school_info.get('recent_trends', 'Info Not Available')}")

    # Step 3 – Full Analysis
    st.markdown("---")
    st.markdown("### 📊 Strategic Overview")
    st.write("Full analysis will be displayed here based on loaded data.")

    # Placeholder for OL Scheme and QB Targeting (from modules)
    st.markdown("---")
    st.markdown("### 🏈 Tactical Modules Snapshots")
    st.write(analyze_ol(school_info))
    st.write(analyze_qb(school_info))
