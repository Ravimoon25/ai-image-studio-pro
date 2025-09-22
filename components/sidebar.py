import streamlit as st
import json

def render_sidebar():
    """Render sidebar with navigation and stats"""
    with st.sidebar:
        st.title("Dashboard")
        
        # Usage statistics
        gen_count = len(st.session_state.generation_history)
        edit_count = len(st.session_state.edit_history)
        analysis_count = len(st.session_state.analysis_history)
        
        st.markdown("**Today's Usage**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Generations", gen_count)
            st.metric("Analyses", analysis_count)
        with col2:
            st.metric("Edits", edit_count)
            st.metric("Total", gen_count + edit_count + analysis_count)
        
        st.markdown("---")
        
        # Quick actions
        if st.button("Clear All History"):
            st.session_state.generation_history = []
            st.session_state.edit_history = []
            st.session_state.analysis_history = []
            st.success("All history cleared!")
        
        if st.button("Export Usage Data"):
            usage_data = {
                'generations': st.session_state.generation_history,
                'edits': st.session_state.edit_history,
                'analyses': st.session_state.analysis_history
            }
            st.download_button(
                "Download Usage Report",
                json.dumps(usage_data, indent=2),
                "usage_report.json",
                "application/json"
            )
