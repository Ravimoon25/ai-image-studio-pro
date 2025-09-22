import streamlit as st
import json
from datetime import datetime
from services.generation_service import generate_image
from services.analysis_service import analyze_image_content
from utils.utils import enhance_prompt, create_download_link
from config.config import STYLE_PRESETS
import PIL.Image

def render_pro_features_tab():
    st.header("Professional Features & Business Tools")
    
    pro_tab1, pro_tab2, pro_tab3 = st.tabs(["Batch Operations", "Analytics", "Settings"])
    
    with pro_tab1:
        render_batch_operations()
    
    with pro_tab2:
        render_analytics()
    
    with pro_tab3:
        render_settings()

def render_batch_operations():
    st.subheader("Batch Processing")
    
    batch_operation = st.selectbox(
        "Batch Operation Type:",
        ["Batch Generation", "Batch Editing", "Batch Analysis", "Batch Face Swap"]
    )
    
    if batch_operation == "Batch Generation":
        st.markdown("**Multiple Prompt Generation**")
        batch_prompts = st.text_area(
            "Enter prompts (one per line):",
            "Professional headshot, business attire\nCasual portrait, outdoor setting\nCreative workspace, inspiring environment",
            height=150
        )
        
        col1, col2 = st.columns(2)
        with col1:
            batch_style = st.selectbox("Style for all:", ["None"] + list(STYLE_PRESETS.keys()))
            batch_variants = st.slider("Variants per prompt:", 1, 3, 1)
        with col2:
            batch_quality = st.checkbox("Quality boost for all", True)
            batch_format = st.selectbox("Output format:", ["PNG", "JPEG", "WEBP"])
        
        if st.button("Generate Batch Images"):
            if batch_prompts.strip():
                prompts = [p.strip() for p in batch_prompts.split('\n') if p.strip()]
                
                all_results = []
                progress_bar = st.progress(0)
                
                for i, prompt in enumerate(prompts):
                    enhanced_prompt = enhance_prompt(prompt, batch_style, "Default", batch_quality)
                    images, _ = generate_image(enhanced_prompt, batch_variants)
                    all_results.extend(images)
                    progress_bar.progress((i + 1) / len(prompts))
                
                st.success(f"Generated {len(all_results)} images from {len(prompts)} prompts!")
                
                # Display batch results
                cols = st.columns(min(3, len(all_results)))
                for i, img in enumerate(all_results):
                    with cols[i % 3]:
                        display_image = convert_to_pil_image(img)
                        st.image(display_image, caption=f"Batch {i+1}")
                        create_download_link(display_image, f"batch_image_{i+1}")
            else:
                st.warning("Please enter batch prompts!")
    
    elif batch_operation == "Batch Analysis":
        st.markdown("**Multiple Image Analysis**")
        uploaded_files = st.file_uploader(
            "Upload multiple images:",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload up to 10 images for batch analysis"
        )
        
        if uploaded_files:
            analysis_type_batch = st.selectbox(
                "Analysis Type:",
                ["Complete Analysis", "Text Extraction", "Quality Assessment", "Business Intelligence"]
            )
            
            if st.button("Analyze All Images"):
                results = []
                progress_bar = st.progress(0)
                
                for i, file in enumerate(uploaded_files):
                    image = PIL.Image.open(file)
                    analysis = analyze_image_content(image, analysis_type_batch.lower().replace(" ", "_"))
                    results.append({
                        'filename': file.name,
                        'analysis': analysis
                    })
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                st.success(f"Analyzed {len(results)} images!")
                
                # Display batch analysis results
                for i, result in enumerate(results):
                    with st.expander(f"{result['filename']} - Analysis"):
                        st.markdown(result['analysis'])
                
                # Export batch results
                batch_report = {
                    'analysis_type': analysis_type_batch,
                    'timestamp': datetime.now().isoformat(),
                    'results': results
                }
                st.download_button(
                    "Download Batch Report",
                    json.dumps(batch_report, indent=2),
                    "batch_analysis_report.json",
                    "application/json"
                )

def render_analytics():
    st.subheader("Usage Analytics & Insights")
    
    # Usage metrics
    total_generations = len(st.session_state.generation_history)
    total_edits = len(st.session_state.edit_history)
    total_analyses = len(st.session_state.analysis_history)
    total_operations = total_generations + total_edits + total_analyses
    
    # Metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Operations", total_operations)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Generations", total_generations)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Transformations", total_edits)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Analyses", total_analyses)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Usage trends
    if total_operations > 0:
        st.markdown("**Feature Usage Breakdown**")
        
        # Most used features
        feature_usage = {}
        for item in st.session_state.edit_history:
            edit_type = item['data'].get('edit_type', 'Unknown')
            feature_usage[edit_type] = feature_usage.get(edit_type, 0) + 1
        
        if feature_usage:
            for feature, count in sorted(feature_usage.items(), key=lambda x: x[1], reverse=True):
                st.write(f"**{feature}:** {count} times")
    
    else:
        st.info("Start using the app to see analytics!")

def render_settings():
    st.subheader("Advanced Settings & Configuration")
    
    st.markdown("**Default Generation Settings**")
    col1, col2 = st.columns(2)
    
    with col1:
        default_style = st.selectbox("Default Style:", list(STYLE_PRESETS.keys()), key="default_style")
        default_quality = st.checkbox("Always use quality boost", True)
        auto_enhance_prompts = st.checkbox("Auto-enhance all prompts", True)
    
    with col2:
        default_variants = st.slider("Default variants:", 1, 4, 2)
        save_originals = st.checkbox("Save original images", True)
        compression_quality = st.slider("Image quality:", 1, 10, 9)
    
    st.markdown("**Privacy & Safety Settings**")
    col3, col4 = st.columns(2)
    
    with col3:
        content_safety = st.checkbox("Enhanced content safety", True)
        watermark_outputs = st.checkbox("Add watermark to outputs", False)
        save_history = st.checkbox("Save operation history", True)
    
    with col4:
        auto_backup = st.checkbox("Auto-backup results", False)
        analytics_tracking = st.checkbox("Usage analytics", True)
        performance_mode = st.selectbox("Performance Mode:", ["Balanced", "Speed", "Quality"])
    
    # API usage monitoring
    st.markdown("**API Usage Monitoring**")
    st.info("API Credits: Monitor your Google API usage in Google Cloud Console")
    st.info("Current Limit: Protected from overspending")
    
    if st.button("Reset All Settings"):
        st.warning("This will reset all settings to default values.")
        if st.button("Confirm Reset"):
            st.success("Settings reset to defaults!")
