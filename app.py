"""
AI Image Studio Pro - Complete AI-Powered Image Generation, Editing & Analysis Platform
"""

import streamlit as st
from utils.utils import init_session_state, get_css_styles
from components.sidebar import render_sidebar
from components.generation_tab import render_generation_tab
from components.editing_tab import render_editing_tab
from components.analysis_tab import render_analysis_tab
from components.history_tab import render_history_tab
from components.pro_features_tab import render_pro_features_tab

# Page configuration
st.set_page_config(
    page_title="AI Image Studio Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main application function"""
    # Apply CSS styles
    st.markdown(get_css_styles(), unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # App header
    st.markdown("""
    <div class="feature-card">
        <h1>🎨 AI Image Studio Pro</h1>
        <p>Complete AI-Powered Image Generation, Editing & Analysis Platform</p>
        <p><strong>68+ Professional Features | Mobile Optimized | Enterprise Ready</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎭 Generate", 
        "✏️ Edit & Transform", 
        "🔍 Analyze & Extract", 
        "📚 History & Templates",
        "💡 Pro Features"
    ])
    
    with tab1:
        render_generation_tab()
    
    with tab2:
        render_editing_tab()
    
    with tab3:
        render_analysis_tab()
    
    with tab4:
        render_history_tab()
    
    with tab5:
        render_pro_features_tab()
    
    # App footer
    render_footer()

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem;">
        <h3>🚀 Complete AI Image Studio</h3>
        <p><strong>68+ Features:</strong> Generation • Editing • Face Swap • Body Modification • Analysis • OCR</p>
        <p><em>Professional-grade AI image processing for businesses and creators</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #6b7280; font-size: 0.9rem;">
        <p><strong>🎨 AI Image Studio Pro</strong> - Your complete AI-powered image solution</p>
        <p>Generation • Transformation • Enhancement • Analysis • Extraction</p>
        <p>Built with ❤️ using Streamlit + Google Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
