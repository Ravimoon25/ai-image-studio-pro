# Configuration file for AI Image Studio Pro
import streamlit as st
from google import genai

# Model configuration
MODEL_ID = "gemini-2.5-flash-image-preview"

@st.cache_resource
def get_client():
    """Initialize Gemini client with error handling"""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize AI client: {str(e)}")
        st.stop()

# Style and content options (moved to individual files to avoid circular imports)
