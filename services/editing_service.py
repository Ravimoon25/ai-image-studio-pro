from google.genai import types
import streamlit as st
from google import genai
import io
import PIL.Image

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

def process_api_image(image_part):
    """Process image from API response and ensure proper PIL format"""
    try:
        if hasattr(image_part, 'as_image'):
            img = image_part.as_image()
            if img:
                # Ensure proper PIL Image format
                if not hasattr(img, 'format') or img.format is None:
                    buf = io.BytesIO()
                    img.save(buf, format='PNG')
                    buf.seek(0)
                    img = PIL.Image.open(buf)
                    img.format = 'PNG'
                return img
    except Exception as e:
        print(f"Error processing API image: {e}")
    return None

def face_swap_images(source_image, target_image, options):
    """Advanced face swap between two images"""
    try:
        client = get_client()
        
        # Build detailed face swap prompt
        prompt = f"""
        Perform a precise face swap operation:
        
        TASK: Take the face from the first image and naturally place it on the person in the second image
        
        REQUIREMENTS:
        - Keep target person's exact body, clothing, pose, and background
        - Swap only the facial features (eyes, nose, mouth, face shape)
        - Match skin tone and lighting naturally
        - Preserve target's hairstyle unless specified
        - Ensure proper face size and angle alignment
        - Create seamless, realistic integration
        - Maintain image quality and resolution
        
        QUALITY SETTINGS:
        - Blend mode: {options.get('blend_quality', 'natural')}
        - Skin tone matching: {options.get('skin_match', 'automatic')}
        - Hair preservation: {options.get('preserve_hair', True)}
        - Expression: {options.get('expression', 'keep target expression')}
        
        Make it look completely natural and professional.
        """
        
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, source_image, target_image],
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    )
                ]
            )
        )
        
        for part in response.parts:
            result_image = process_api_image(part)
            if result_image:
                return result_image, "Face swap completed successfully!"
        
        return None, "Face swap failed to generate result"
    except Exception as e:
        return None, f"Face swap error: {str(e)}"

def advanced_edit_image(input_image, edit_type, options):
    """Enhanced editing with all transformation capabilities"""
    try:
        client = get_client()
        
        # Build specific prompts for different edit types
        if edit_type == "outfit_change":
            prompt = f"Change the person's clothing to {options['clothing']}, keep same person, face, pose and background. {options.get('additional', '')}"
            
        elif edit_type == "pose_change":
            prompt = f"Modify the person's pose to {options['pose']} with {options['expression']} facial expression. Keep same person, clothing, and background."
            
        elif edit_type == "face_enhancement":
            prompt = f"Enhance the person's face: {options['enhancement']}. Keep everything else exactly the same. Make it look natural and professional."
            
        elif edit_type == "body_modification":
            prompt = f"Modify the person's body: {options['modification']}. Keep face, clothing style, and background the same. Make it look natural and realistic."
            
        elif edit_type == "background_change":
            prompt = f"Change the background to {options['background']}. Keep the person(s) exactly the same with proper lighting and shadows."
            
        elif edit_type == "object_control":
            if options['action'] == 'remove':
                prompt = f"Remove {options['object']} from the image. Fill the space naturally with appropriate background."
            elif options['action'] == 'add':
                prompt = f"Add {options['object']} to the image in a natural way that fits the scene and lighting."
            else:
                prompt = f"Replace {options['old_object']} with {options['new_object']} naturally in the scene."
                
        elif edit_type == "complete_makeover":
            prompt = f"Complete transformation: change clothing to {options['clothing']}, modify pose to {options['pose']}, enhance face with {options['face_enhancement']}, expression to {options['expression']}. Keep same person and background."
            
        elif edit_type == "style_transfer":
            prompt = f"Transform this image to {options['style']} style while maintaining all subjects and composition."
            
        else:  # custom edit
            prompt = options.get('custom_prompt', 'Enhance this image professionally')
        
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, input_image],
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE,
                    )
                ]
            )
        )
        
        for part in response.parts:
            result_image = process_api_image(part)
            if result_image:
                return result_image, "Image transformation completed successfully!"
        
        return None, "No edited image generated"
    except Exception as e:
        return None, f"Editing error: {str(e)}"
