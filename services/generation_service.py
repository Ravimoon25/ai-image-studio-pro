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

def generate_image(prompt, num_variants=1):
    """Generate image(s) from text prompt"""
    try:
        client = get_client()
        results = []
        
        for i in range(num_variants):
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config=types.GenerateContentConfig(
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                        )
                    ],
                    response_modalities=['Text', 'Image']
                )
            )
            
            # Process the response more carefully
            for part in response.parts:
                if hasattr(part, 'as_image'):
                    try:
                        # Get the image from the response
                        img = part.as_image()
                        if img:
                            # Convert to proper PIL Image with format attribute
                            if not hasattr(img, 'format') or img.format is None:
                                # Save to buffer and reload to ensure proper format
                                buf = io.BytesIO()
                                img.save(buf, format='PNG')
                                buf.seek(0)
                                img = PIL.Image.open(buf)
                                img.format = 'PNG'  # Explicitly set format
                            results.append(img)
                            break
                    except Exception as e:
                        print(f"Error processing image part: {e}")
                        continue
        
        return results, "Images generated successfully!"
    except Exception as e:
        return [], f"Generation error: {str(e)}"
