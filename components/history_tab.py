import streamlit as st
import json

def render_history_tab():
    st.header("Activity History & Smart Templates")
    
    history_tab1, history_tab2, history_tab3, template_tab = st.tabs([
        "Generations", 
        "Transformations", 
        "Analysis", 
        "Templates"
    ])
    
    with history_tab1:
        st.subheader("Generation History")
        if st.session_state.generation_history:
            for i, item in enumerate(st.session_state.generation_history):
                with st.expander(f"Generation {i+1} - {item['timestamp']}"):
                    data = item['data']
                    st.write(f"**Prompt:** {data.get('prompt', 'N/A')}")
                    st.write(f"**Style:** {data.get('style', 'None')}")
                    st.write(f"**Variants:** {data.get('variants', 1)}")
                    st.write(f"**Images Created:** {data.get('count', 1)}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Regenerate", key=f"regen_{i}"):
                            st.session_state.template_prompt = data.get('prompt', '')
                            st.info("Prompt copied! Go to Generate tab.")
                    with col2:
                        if st.button(f"Copy Prompt", key=f"copy_gen_{i}"):
                            st.code(data.get('prompt', ''))
        else:
            st.info("No generations yet. Create your first image in the Generate tab!")
    
    with history_tab2:
        st.subheader("Transformation History")
        if st.session_state.edit_history:
            for i, item in enumerate(st.session_state.edit_history):
                with st.expander(f"Transform {i+1} - {item['timestamp']}"):
                    data = item['data']
                    st.write(f"**Type:** {data.get('edit_type', 'Unknown')}")
                    st.write(f"**Success:** {'✅' if data.get('success') else '❌'}")
                    st.write(f"**Timestamp:** {data.get('timestamp', 'N/A')}")
                    
                    if st.button(f"View Details", key=f"edit_details_{i}"):
                        st.json(data.get('options', {}))
        else:
            st.info("No transformations yet. Edit your first image in the Transform tab!")
    
    with history_tab3:
        st.subheader("Analysis History")
        if st.session_state.analysis_history:
            for i, item in enumerate(st.session_state.analysis_history):
                with st.expander(f"Analysis {i+1} - {item['timestamp']}"):
                    data = item['data']
                    st.write(f"**Analysis Type:** {data.get('analysis_type', 'Unknown')}")
                    st.write(f"**Success:** {'✅' if data.get('success') else '❌'}")
                    
                    if st.button(f"Re-run Analysis", key=f"rerun_analysis_{i}"):
                        st.info("Go to Analysis tab to perform new analysis!")
        else:
            st.info("No analysis performed yet. Analyze your first image in the Analysis tab!")
    
    with template_tab:
        st.subheader("Smart Templates & Presets")
        
        template_categories = {
            "Professional Business": [
                "Executive portrait in navy suit, confident expression, office background",
                "Professional businesswoman in blazer, warm smile, corporate environment",
                "Team headshot, business casual, modern office setting",
                "LinkedIn profile photo, professional attire, neutral background"
            ],
            "Creative & Artistic": [
                "Artist in creative studio, inspiring workspace, natural lighting",
                "Designer at work, modern creative environment, focused expression",
                "Creative professional, artistic background, thoughtful pose",
                "Innovation leader, tech startup environment, confident stance"
            ],
            "Social Media Ready": [
                "Instagram influencer style, trendy outfit, engaging smile",
                "Social media content creator, colorful background, dynamic pose",
                "Lifestyle blogger aesthetic, casual chic, authentic moment",
                "Content creator workspace, modern setup, professional casual"
            ],
            "Character & Fantasy": [
                "Superhero character, dynamic action pose, heroic background",
                "Fantasy warrior, medieval armor, epic landscape",
                "Sci-fi character, futuristic outfit, space environment",
                "Anime character, vibrant colors, stylized background"
            ],
            "Cultural & Traditional": [
                "Traditional Indian bride, ornate lehenga, wedding decorations",
                "Professional in cultural attire, modern office, proud expression",
                "Festival celebration, traditional clothing, joyful atmosphere",
                "Cultural leader, traditional dress, dignified pose"
            ]
        }
        
        for category, templates in template_categories.items():
            with st.expander(f"{category}"):
                for j, template in enumerate(templates):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"{template}")
                    with col2:
                        if st.button("Copy", key=f"template_{category}_{j}", help="Copy to Generate tab"):
                            st.session_state.template_prompt = template
                            st.success("Copied!")
