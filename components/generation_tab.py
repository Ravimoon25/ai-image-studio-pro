
import streamlit as st
import PIL.Image
from datetime import datetime
from config.config import STYLE_PRESETS, ASPECT_RATIOS
from services.generation_service import generate_image
from utils.utils import enhance_prompt, save_to_history, create_download_link

def render_generation_tab():
    st.header("Advanced Image Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main prompt input
        prompt = st.text_area(
            "Describe your image in detail:",
            "A confident professional woman in business attire, standing in modern office, natural lighting, professional photography style",
            height=120,
            help="Be specific about people, clothing, poses, environment, lighting, and style for best results"
        )
        
        # Advanced generation options
        st.markdown("**Generation Settings**")
        
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            style = st.selectbox("Art Style:", ["None"] + list(STYLE_PRESETS.keys()))
            aspect_ratio = st.selectbox("Aspect Ratio:", ["Default"] + list(ASPECT_RATIOS.keys()))
        
        with col1b:
            num_variants = st.slider("Variations:", 1, 4, 2, help="Generate multiple versions")
            quality_boost = st.checkbox("Quality Enhancement", True)
        
        with col1c:
            batch_mode = st.checkbox("Batch Mode", False, help="Generate images from multiple prompts")
            auto_enhance = st.checkbox("Auto-Enhance Prompt", True)
        
        # Batch generation option
        if batch_mode:
            batch_prompts = st.text_area(
                "Batch Prompts (one per line):",
                "Professional headshot\nCasual outdoor portrait\nBusiness meeting photo",
                height=100
            )
        
        # Generate button
        if st.button("Generate Images", type="primary"):
            if prompt.strip():
                prompts_to_process = []
                
                if batch_mode and batch_prompts.strip():
                    prompts_to_process = [p.strip() for p in batch_prompts.split('\n') if p.strip()]
                else:
                    enhanced_prompt = enhance_prompt(prompt, style, aspect_ratio, quality_boost) if auto_enhance else prompt
                    prompts_to_process = [enhanced_prompt]
                
                all_images = []
                
                for i, current_prompt in enumerate(prompts_to_process):
                    with st.spinner(f"Generating images {i+1}/{len(prompts_to_process)}..."):
                        images, message = generate_image(current_prompt, num_variants)
                        all_images.extend(images)
                
                if all_images:
                    st.success(f"Generated {len(all_images)} images successfully!")
                    
                    # Display images in responsive grid
                    if len(all_images) == 1:
                        st.image(all_images[0], use_column_width=True)
                        create_download_link(all_images[0], "generated_image")
                    else:
                        # Grid display for multiple images
                        cols_per_row = min(3, len(all_images))
                        for i in range(0, len(all_images), cols_per_row):
                            cols = st.columns(cols_per_row)
                            for j, img in enumerate(all_images[i:i+cols_per_row]):
                                with cols[j]:
                                    st.image(img, caption=f"Image {i+j+1}")
                                    create_download_link(img, f"image_{i+j+1}")
                    
                    # Batch download option
                    if len(all_images) > 1:
                        if st.button("Download All as ZIP"):
                            st.info("ZIP download feature coming soon!")
                    
                    # Save to history
                    save_to_history('generation', {
                        'prompt': prompt,
                        'style': style,
                        'variants': num_variants,
                        'batch_mode': batch_mode,
                        'count': len(all_images)
                    })
                else:
                    st.error("Failed to generate images. Please try again.")
            else:
                st.warning("Please enter a description!")
    
    with col2:
        st.markdown("**Quick Templates**")
        
        template_categories = {
            "Professional": [
                "Business headshot, confident expression",
                "Corporate team photo, professional attire",
                "Executive portrait, formal background",
                "LinkedIn profile photo, approachable smile"
            ],
            "Creative": [
                "Artistic portrait, creative lighting",
                "Fashion model pose, stylish outfit",
                "Creative workspace, inspiring environment",
                "Artistic collaboration, team creativity"
            ],
            "Social Media": [
                "Instagram-ready portrait, trendy style",
                "Lifestyle photo, casual but polished",
                "Influencer content, engaging pose",
                "Story-worthy moment, authentic feel"
            ],
            "Character": [
                "Fantasy character, magical setting",
                "Superhero pose, dynamic action",
                "Historical figure, period clothing",
                "Anime character, vibrant colors"
            ]
        }
        
        for category, templates in template_categories.items():
            with st.expander(category):
                for template in templates:
                    if st.button(template[:30] + "...", key=f"template_{template[:15]}", help=template):
                        st.session_state.template_prompt = template
                        st.rerun()
