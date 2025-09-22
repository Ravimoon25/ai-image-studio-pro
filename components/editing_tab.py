import streamlit as st
import PIL.Image
from datetime import datetime
from services.editing_service import face_swap_images, advanced_edit_image
from utils.utils import save_to_history, create_download_link, convert_to_pil_image

def get_config_options():
    """Get all configuration options"""
    return {
        'CLOTHING_OPTIONS': {
            "Business Formal": "professional business suit, formal corporate attire, executive styling",
            "Casual Wear": "comfortable jeans and t-shirt, relaxed everyday clothing",
            "Elegant Evening": "sophisticated evening dress, formal party attire, glamorous",
            "Traditional Indian": "beautiful traditional Indian clothing, saree, kurta, cultural dress",
            "Wedding Attire": "elegant wedding dress, formal wedding suit, bridal styling",
            "Sportswear": "athletic wear, gym clothes, sports uniform, active lifestyle",
            "Winter Wear": "warm winter coat, cozy sweater, seasonal layered clothing",
            "Beach Wear": "summer beach outfit, light breezy clothing, vacation style",
            "Vintage Style": "retro vintage clothing from past decades, classic fashion",
            "Designer Fashion": "high-end designer clothing, luxury fashion, couture styling"
        },
        'POSE_OPTIONS': {
            "Confident Standing": "confident upright posture, hands on hips, strong authoritative stance",
            "Relaxed Casual": "relaxed natural pose, comfortable casual body language",
            "Professional Portrait": "professional headshot pose, business appropriate, executive presence",
            "Dynamic Action": "energetic dynamic pose, movement and life, active positioning",
            "Sitting Elegant": "graceful sitting position, elegant refined posture",
            "Walking Forward": "confident walking stride, forward motion, purposeful movement",
            "Arms Crossed": "confident pose with arms crossed, assertive professional stance",
            "Waving Hello": "friendly waving gesture, welcoming approachable pose",
            "Thinking Pose": "thoughtful pose, hand on chin, contemplative positioning",
            "Victory Pose": "celebratory victory stance, arms raised, triumphant gesture"
        },
        'FACIAL_EXPRESSIONS': {
            "Natural Smile": "genuine natural smile, warm and friendly expression",
            "Confident Look": "confident serious expression, professional authoritative demeanor", 
            "Joyful Laugh": "happy laughing expression, pure joy and happiness",
            "Thoughtful": "contemplative thoughtful expression, intelligent focused look",
            "Surprised": "surprised expression, wide eyes, astonished look",
            "Peaceful": "calm peaceful expression, serene tranquil look"
        },
        'BACKGROUND_OPTIONS': {
            "Smart Remove": "completely remove background, create transparent PNG",
            "Studio Professional": "professional studio lighting, clean neutral backdrop",
            "Modern Office": "contemporary office environment, professional workspace",
            "Outdoor Natural": "beautiful outdoor natural setting, parks or landscapes",
            "Urban City": "modern city environment, urban professional setting",
            "Home Lifestyle": "cozy home interior, comfortable living space",
            "Product Studio": "e-commerce white background, clean product photography",
            "Fantasy World": "magical fantasy environment, creative artistic backdrop",
            "Seasonal Theme": "seasonal environment, holiday or weather-themed backdrop"
        },
        'FACE_ENHANCEMENT': {
            "Skin Perfection": "smooth flawless skin, remove blemishes naturally, even skin tone",
            "Eye Enhancement": "brighter sparkling eyes, natural eye enhancement", 
            "Smile Improvement": "perfect natural smile, teeth whitening, confident expression",
            "Hair Styling": "perfect hairstyle, natural hair enhancement, styled look",
            "Overall Beauty": "natural beauty enhancement, subtle professional improvement",
            "Age Adjustment": "youthful appearance, age-appropriate enhancement"
        },
        'BODY_MODIFICATIONS': {
            "Fitness Transform": "athletic toned body, fit healthy appearance, natural muscle definition",
            "Posture Improvement": "confident straight posture, professional body language",
            "Height Enhancement": "taller proportional appearance, elegant stature",
            "Body Proportions": "balanced natural body proportions, harmonious physique",
            "Clothing Fit": "perfectly fitted clothing, tailored professional appearance"
        }
    }

def render_editing_tab():
    st.header("Complete Image Transformation Studio")
    
    # Image upload
    uploaded_image = st.file_uploader(
        "Upload image to transform:",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear, high-quality image for best transformation results"
    )
    
    if uploaded_image:
        image = PIL.Image.open(uploaded_image)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Main transformation type selection
        st.markdown("**Choose Transformation Type:**")
        edit_type = st.radio(
            "Select transformation:",
            [
                "Change Outfit",
                "Change Pose & Expression", 
                "Face Swap",
                "Face Enhancement",
                "Body Modification",
                "Background Control",
                "Object Management",
                "Complete Makeover",
                "Style Transfer",
                "Custom Transformation"
            ],
            horizontal=False
        )
        
        # Get transformation options based on edit type
        options = get_transformation_options(edit_type, image)
        
        # Transform button
        transform_button_text = {
            "Change Outfit": "Transform Outfit",
            "Change Pose & Expression": "Change Pose",
            "Face Swap": "Swap Faces", 
            "Face Enhancement": "Enhance Face",
            "Body Modification": "Transform Body",
            "Background Control": "Change Background",
            "Object Management": "Modify Objects",
            "Complete Makeover": "Complete Makeover",
            "Style Transfer": "Apply Style",
            "Custom Transformation": "Transform"
        }
        
        if st.button(transform_button_text[edit_type], type="primary"):
            # Special handling for face swap
            if edit_type == "Face Swap":
                if 'source_image' in options and options['source_image'] is not None:
                    with st.spinner("Performing face swap..."):
                        result = face_swap_images(options['source_image'], image, options)
                else:
                    st.warning("Please upload a source face image for face swap!")
                    return
            else:
                # Regular transformation
                edit_type_map = {
                    "Change Outfit": "outfit_change",
                    "Change Pose & Expression": "pose_change",
                    "Face Enhancement": "face_enhancement", 
                    "Body Modification": "body_modification",
                    "Background Control": "background_change",
                    "Object Management": "object_control",
                    "Complete Makeover": "complete_makeover",
                    "Style Transfer": "style_transfer",
                    "Custom Transformation": "custom_edit"
                }
                
                with st.spinner(f"Performing {edit_type.lower()}..."):
                    result = advanced_edit_image(image, edit_type_map[edit_type], options)
            
            edited_image, message = result
            
            if edited_image:
                st.success(f"{message}")
                
                # Before/After comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image, caption="Before", use_container_width=True)
                with col2:
                    # Convert to PIL Image if needed
                    display_image = convert_to_pil_image(edited_image)
                    st.image(display_image, caption="After", use_container_width=True)
                
                # Download options
                create_download_link(display_image, f"transformed_{edit_type.replace(' ', '_').lower()}")
                
                # Save to history
                save_to_history('edit', {
                    'edit_type': edit_type,
                    'options': str(options),
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                })
                
            else:
                st.error(f"{message}")

def get_transformation_options(edit_type, image):
    """Get options based on transformation type"""
    config = get_config_options()
    options = {}
    
    if edit_type == "Change Outfit":
        st.markdown("**Outfit Transformation**")
        col1, col2 = st.columns(2)
        
        with col1:
            clothing_style = st.selectbox("New Outfit:", list(config['CLOTHING_OPTIONS'].keys()))
            color_preference = st.text_input("Color preference:", "")
        
        with col2:
            fit_style = st.selectbox("Fit Style:", ["Well-fitted", "Loose", "Tight", "Flowing", "Tailored"])
            occasion = st.selectbox("Occasion:", ["Casual", "Professional", "Formal", "Party", "Traditional", "Sports"])
        
        options = {
            'clothing': config['CLOTHING_OPTIONS'][clothing_style],
            'additional': f"in {color_preference} color" if color_preference else ""
        }
        
    elif edit_type == "Change Pose & Expression":
        st.markdown("**Pose & Expression Control**")
        col1, col2 = st.columns(2)
        
        with col1:
            pose_style = st.selectbox("New Pose:", list(config['POSE_OPTIONS'].keys()))
            expression = st.selectbox("Facial Expression:", list(config['FACIAL_EXPRESSIONS'].keys()))
        
        with col2:
            energy_level = st.selectbox("Energy Level:", ["Calm", "Moderate", "High Energy", "Dynamic"])
            confidence_level = st.selectbox("Confidence:", ["Natural", "Confident", "Very Confident", "Relaxed"])
        
        options = {
            'pose': config['POSE_OPTIONS'][pose_style],
            'expression': config['FACIAL_EXPRESSIONS'][expression]
        }
        
    elif edit_type == "Face Swap":
        st.markdown("**Advanced Face Swap**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Source Face (Face to Copy)**")
            source_face = st.file_uploader(
                "Upload source face photo:",
                type=['png', 'jpg', 'jpeg'],
                key="source_face_upload",
                help="Clear frontal face photo works best"
            )
            if source_face:
                source_img = PIL.Image.open(source_face)
                st.image(source_img, caption="Source Face", use_container_width=True)
        
        with col2:
            st.markdown("**Target Image (Body to Keep)**")
            st.info("Using the main uploaded image as target body")
            st.image(image, caption="Target Body", use_container_width=True)
        
        # Face swap options
        preserve_hair = st.checkbox("Keep target's hairstyle", True)
        match_skin_tone = st.checkbox("Auto-match skin tone", True)
        
        options = {
            'source_image': source_img if source_face else None,
            'preserve_hair': preserve_hair,
            'skin_match': match_skin_tone,
            'blend_quality': 'natural'
        }
        
    elif edit_type == "Face Enhancement":
        st.markdown("**Professional Face Enhancement**")
        
        enhancement_category = st.selectbox(
            "Enhancement Focus:",
            list(config['FACE_ENHANCEMENT'].keys())
        )
        
        enhancement_intensity = st.slider("Enhancement intensity:", 1, 10, 5)
        natural_look = st.checkbox("Keep natural appearance", True)
        
        options = {
            'enhancement': config['FACE_ENHANCEMENT'][enhancement_category],
            'intensity': enhancement_intensity,
            'natural': natural_look
        }
        
    elif edit_type == "Body Modification":
        st.markdown("**Body Shape & Fitness Enhancement**")
        
        modification_type = st.selectbox("Modification Focus:", list(config['BODY_MODIFICATIONS'].keys()))
        modification_intensity = st.slider("Modification intensity:", 1, 10, 4)
        keep_natural = st.checkbox("Maintain natural look", True)
        
        options = {
            'modification': config['BODY_MODIFICATIONS'][modification_type],
            'intensity': modification_intensity,
            'natural': keep_natural
        }
        
    elif edit_type == "Background Control":
        st.markdown("**Background Transformation**")
        
        background_action = st.selectbox(
            "Background Action:",
            ["Remove Background", "Replace Background", "Enhance Background"]
        )
        
        if background_action == "Replace Background":
            new_background = st.selectbox("New Background:", list(config['BACKGROUND_OPTIONS'].keys()))
            lighting_match = st.checkbox("Match lighting to new background", True)
            bg_description = config['BACKGROUND_OPTIONS'][new_background]
        else:
            bg_description = ""
            lighting_match = True
        
        options = {
            'action': background_action,
            'background': bg_description,
            'lighting_match': lighting_match
        }
        
    elif edit_type == "Custom Transformation":
        st.markdown("**Custom Transformation**")
        custom_prompt = st.text_area(
            "Describe the transformation:",
            "Enhance the overall appearance, improve lighting, and make it more professional",
            height=100
        )
        
        options = {
            'custom_prompt': custom_prompt
        }
    
    else:
        # Default options for other transformation types
        options = {}
    
    return options

def render_editing_tab():
    st.header("Complete Image Transformation Studio")
    
    # Image upload
    uploaded_image = st.file_uploader(
        "Upload image to transform:",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear, high-quality image for best transformation results"
    )
    
    if uploaded_image:
        image = PIL.Image.open(uploaded_image)
        st.image(image, caption="Original Image", use_container_width=True)
        
        # Main transformation type selection
        st.markdown("**Choose Transformation Type:**")
        edit_type = st.radio(
            "Select transformation:",
            [
                "Change Outfit",
                "Change Pose & Expression", 
                "Face Swap",
                "Face Enhancement",
                "Body Modification",
                "Background Control",
                "Object Management",
                "Complete Makeover",
                "Style Transfer",
                "Custom Transformation"
            ],
            horizontal=False
        )
        
        # Get transformation options based on edit type
        options = get_transformation_options(edit_type, image)
        
        # Transform button
        transform_button_text = {
            "Change Outfit": "Transform Outfit",
            "Change Pose & Expression": "Change Pose",
            "Face Swap": "Swap Faces", 
            "Face Enhancement": "Enhance Face",
            "Body Modification": "Transform Body",
            "Background Control": "Change Background",
            "Object Management": "Modify Objects",
            "Complete Makeover": "Complete Makeover",
            "Style Transfer": "Apply Style",
            "Custom Transformation": "Transform"
        }
        
        if st.button(transform_button_text[edit_type], type="primary"):
            # Special handling for face swap
            if edit_type == "Face Swap":
                if 'source_image' in options and options['source_image'] is not None:
                    with st.spinner("Performing face swap..."):
                        result = face_swap_images(options['source_image'], image, options)
                else:
                    st.warning("Please upload a source face image for face swap!")
                    return
            else:
                # Regular transformation
                edit_type_map = {
                    "Change Outfit": "outfit_change",
                    "Change Pose & Expression": "pose_change",
                    "Face Enhancement": "face_enhancement", 
                    "Body Modification": "body_modification",
                    "Background Control": "background_change",
                    "Object Management": "object_control",
                    "Complete Makeover": "complete_makeover",
                    "Style Transfer": "style_transfer",
                    "Custom Transformation": "custom_edit"
                }
                
                with st.spinner(f"Performing {edit_type.lower()}..."):
                    result = advanced_edit_image(image, edit_type_map[edit_type], options)
            
            edited_image, message = result
            
            if edited_image:
                st.success(f"{message}")
                
                # Before/After comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image, caption="Before", use_container_width=True)
                with col2:
                    # Convert to PIL Image if needed
                    display_image = convert_to_pil_image(edited_image)
                    st.image(display_image, caption="After", use_container_width=True)
                
                # Download options
                create_download_link(display_image, f"transformed_{edit_type.replace(' ', '_').lower()}")
                
                # Save to history
                save_to_history('edit', {
                    'edit_type': edit_type,
                    'options': str(options),
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                })
                
            else:
                st.error(f"{message}")

def get_transformation_options(edit_type, image):
    """Get options based on transformation type"""
    options = {}
    
    if edit_type == "Change Outfit":
        st.markdown("**Outfit Transformation**")
        col1, col2 = st.columns(2)
        
        with col1:
            clothing_style = st.selectbox("New Outfit:", list(CLOTHING_OPTIONS.keys()))
            color_preference = st.text_input("Color preference:", "")
        
        with col2:
            fit_style = st.selectbox("Fit Style:", ["Well-fitted", "Loose", "Tight", "Flowing", "Tailored"])
            occasion = st.selectbox("Occasion:", ["Casual", "Professional", "Formal", "Party", "Traditional", "Sports"])
        
        options = {
            'clothing': CLOTHING_OPTIONS[clothing_style],
            'additional': f"in {color_preference} color" if color_preference else ""
        }
        
    elif edit_type == "Change Pose & Expression":
        st.markdown("**Pose & Expression Control**")
        col1, col2 = st.columns(2)
        
        with col1:
            pose_style = st.selectbox("New Pose:", list(POSE_OPTIONS.keys()))
            expression = st.selectbox("Facial Expression:", list(FACIAL_EXPRESSIONS.keys()))
        
        with col2:
            energy_level = st.selectbox("Energy Level:", ["Calm", "Moderate", "High Energy", "Dynamic"])
            confidence_level = st.selectbox("Confidence:", ["Natural", "Confident", "Very Confident", "Relaxed"])
        
        options = {
            'pose': POSE_OPTIONS[pose_style],
            'expression': FACIAL_EXPRESSIONS[expression]
        }
        
    elif edit_type == "Face Swap":
        st.markdown("**Advanced Face Swap**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Source Face (Face to Copy)**")
            source_face = st.file_uploader(
                "Upload source face photo:",
                type=['png', 'jpg', 'jpeg'],
                key="source_face_upload",
                help="Clear frontal face photo works best"
            )
            if source_face:
                source_img = PIL.Image.open(source_face)
                st.image(source_img, caption="Source Face", use_container_width=True)
        
        with col2:
            st.markdown("**Target Image (Body to Keep)**")
            st.info("Using the main uploaded image as target body")
            st.image(image, caption="Target Body", use_container_width=True)
        
        # Face swap options
        preserve_hair = st.checkbox("Keep target's hairstyle", True)
        match_skin_tone = st.checkbox("Auto-match skin tone", True)
        
        options = {
            'source_image': source_img if source_face else None,
            'preserve_hair': preserve_hair,
            'skin_match': match_skin_tone,
            'blend_quality': 'natural'
        }
        
    elif edit_type == "Face Enhancement":
        st.markdown("**Professional Face Enhancement**")
        
        enhancement_category = st.selectbox(
            "Enhancement Focus:",
            list(FACE_ENHANCEMENT.keys())
        )
        
        enhancement_intensity = st.slider("Enhancement intensity:", 1, 10, 5)
        natural_look = st.checkbox("Keep natural appearance", True)
        
        options = {
            'enhancement': FACE_ENHANCEMENT[enhancement_category],
            'intensity': enhancement_intensity,
            'natural': natural_look
        }
        
    elif edit_type == "Body Modification":
        st.markdown("**Body Shape & Fitness Enhancement**")
        
        modification_type = st.selectbox("Modification Focus:", list(BODY_MODIFICATIONS.keys()))
        modification_intensity = st.slider("Modification intensity:", 1, 10, 4)
        keep_natural = st.checkbox("Maintain natural look", True)
        
        options = {
            'modification': BODY_MODIFICATIONS[modification_type],
            'intensity': modification_intensity,
            'natural': keep_natural
        }
        
    elif edit_type == "Background Control":
        st.markdown("**Background Transformation**")
        
        background_action = st.selectbox(
            "Background Action:",
            ["Remove Background", "Replace Background", "Enhance Background"]
        )
        
        if background_action == "Replace Background":
            new_background = st.selectbox("New Background:", list(BACKGROUND_OPTIONS.keys()))
            lighting_match = st.checkbox("Match lighting to new background", True)
            bg_description = BACKGROUND_OPTIONS[new_background]
        else:
            bg_description = ""
            lighting_match = True
        
        options = {
            'action': background_action,
            'background': bg_description,
            'lighting_match': lighting_match
        }
        
    elif edit_type == "Custom Transformation":
        st.markdown("**Custom Transformation**")
        custom_prompt = st.text_area(
            "Describe the transformation:",
            "Enhance the overall appearance, improve lighting, and make it more professional",
            height=100
        )
        
        options = {
            'custom_prompt': custom_prompt
        }
    
    else:
        # Default options for other transformation types
        options = {}
    
    return options
