import streamlit as st
import io
from datetime import datetime
import json
import PIL.Image
from config.config import STYLE_PRESETS, ASPECT_RATIOS

def init_session_state():
    """Initialize session state variables"""
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    if 'edit_history' not in st.session_state:
        st.session_state.edit_history = []
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

def convert_to_pil_image(image):
    """Convert various image formats to PIL Image"""
    try:
        # If it's already a PIL Image, return it
        if isinstance(image, PIL.Image.Image):
            return image
        
        # If it's a Gemini AI response with as_image method
        if hasattr(image, 'as_image'):
            try:
                pil_img = image.as_image()
                # Ensure it has the format attribute by saving and reopening
                if pil_img and not hasattr(pil_img, 'format'):
                    buf = io.BytesIO()
                    pil_img.save(buf, format='PNG')
                    buf.seek(0)
                    return PIL.Image.open(buf)
                return pil_img
            except Exception as e:
                st.error(f"Error converting Gemini image: {e}")
                return None
        
        # If it's file-like object
        if hasattr(image, 'read'):
            return PIL.Image.open(image)
        
        # If it's bytes
        if isinstance(image, bytes):
            return PIL.Image.open(io.BytesIO(image))
        
        # Default: try to treat as PIL Image
        return image
        
    except Exception as e:
        st.error(f"Error converting image to PIL format: {e}")
        return None

def enhance_prompt(base_prompt, style, aspect_ratio, quality_boost=True):
    """Enhance user prompt with style and technical improvements"""
    enhanced = base_prompt
    
    if style != "None":
        enhanced = f"{enhanced}, {STYLE_PRESETS[style]}"
    
    if aspect_ratio != "Default":
        enhanced = f"{enhanced}, {ASPECT_RATIOS[aspect_ratio]}"
    
    if quality_boost:
        enhanced = f"{enhanced}, high quality, detailed, professional, sharp focus, well-composed"
    
    return enhanced

def save_to_history(item_type, data):
    """Save operations to history"""
    history_item = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': item_type,
        'data': data
    }
    
    if item_type == 'generation':
        st.session_state.generation_history.insert(0, history_item)
        if len(st.session_state.generation_history) > 20:
            st.session_state.generation_history.pop()
    elif item_type == 'edit':
        st.session_state.edit_history.insert(0, history_item)
        if len(st.session_state.edit_history) > 20:
            st.session_state.edit_history.pop()
    else:  # analysis
        st.session_state.analysis_history.insert(0, history_item)
        if len(st.session_state.analysis_history) > 20:
            st.session_state.analysis_history.pop()

def create_download_link(image, filename):
    """Create download button for images"""
    try:
        # Ensure we have a PIL Image
        pil_image = convert_to_pil_image(image)
        
        buf = io.BytesIO()
        pil_image.save(buf, format='PNG')
        buf.seek(0)
        
        return st.download_button(
            f"Download {filename}",
            buf.getvalue(),
            f"{filename}.png",
            "image/png"
        )
    except Exception as e:
        st.error(f"Error creating download link: {str(e)}")
        return None

def get_css_styles():
    """Return CSS styles for the application"""
    return """
    <style>
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
    }

    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .stTextArea textarea {
        font-size: 16px !important;
        border-radius: 8px;
    }

    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }

    .analysis-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
    }
    </style>
    """
