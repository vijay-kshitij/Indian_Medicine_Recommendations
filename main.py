# To make streamlit cloud sqlite3 dependency compatible
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from indian_rec import run_indian_meds_recommender
import os

# Set the page configuration
st.set_page_config(page_title="Meds Recommender")

# CSS for the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://img.freepik.com/premium-photo/pills-white-background-medicines-tablets-pharmacy-health-healthcare-concept-free-copy-space-your-text-3d-rendering_429124-2113.jpg");
    background-size: 100vw 100vh;
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["About", "Get GROQ API Key", "Recommendation App"])

# Ask the user for the Groq API key
st.sidebar.subheader("Enter your Groq API key")
api_key = st.sidebar.text_input("Groq API Key", type="password")

# Save the API key in session state
if "groq_api_key" not in st.session_state:
    st.session_state["groq_api_key"] = None

if api_key:
    st.session_state["groq_api_key"] = api_key

# About Page
if page == "About":
    st.title("About This App")
    st.write("""
    The Indian Medicine Recommendation System is a tool designed to provide personalized medicine 
    recommendations for common ailments like cold, flu, and fever.   

    The recommendations are based on symptoms like:

    Fever,
    Cough,
    Runny or Stuffy Nose,
    Sore Throat,
    Headache,
    Weakness,
    Body Aches,
    Difficulty Breathing,
    And more...
    
    Please note that the database powering this system contains only 306 medicines, so the recommendations 
    provided may be limited in scope.
    
    However, it is important to note that this project is intended for demonstration purposes only. 
    The recommendations provided by this model should not be considered 100% accurate or definitive. 
    They are not a replacement for professional medical advice. Always consult with a healthcare provider before 
    taking any medication.

    The primary goal of this project is to showcase the development and functionality of a LLM-based recommendation model, 
    as well as highlight my skills in extracting/scraping data, structuring it and prompt engineering. 
    This system should not be taken as a tool for serious medical decision-making but rather as an example of technical capabilities.
    """)


elif page == "Get GROQ API Key":
    st.title("How to Get Your Groq API Key")

    st.write("""
            Follow these steps to obtain an API key to use Groq models:
            """)

    st.subheader("Step 1: Sign Up for a Console Account")
    st.write("""
            First, visit the Groq Cloud website at [console.groq.com](https://console.groq.com) and create an account.
            """)

    st.subheader("Step 2: Log In to Your Account")
    st.write("""
            Once you've signed up, log in to your Groq Console account.
            """)

    st.subheader("Step 3: Navigate to the API Key Section")
    st.write("""
            After logging in, go to the **API Keys** section.
            """)

    st.subheader("Step 4: Generate a New API Key")
    st.write("""
            Click the **Create API Key** button and give it a descriptive name.

            **Important:** You won't be able to view the API key again once you leave the page, so make sure to save it somewhere safe.

            Treat your API key like a password and keep it confidential. If it falls into the wrong hands, others may be able to use it to access Groq services using your account.
            """)

    st.subheader("Step 5: Enter Your API Key in the App")
    st.write("""
            After generating the API key, enter it into the input field provided in this app to start using the Recommendation Model.
            """)

# Indian Meds Recommender Page
elif page == "Recommendation App":
    if st.session_state["groq_api_key"]:
        run_indian_meds_recommender(st.session_state["groq_api_key"])  # Pass the API key to the recommender function
    else:
        st.error("Please enter your Groq API key in the sidebar and press enter.\nFor instructions, see the 'Get GROQ API Key' section.")


