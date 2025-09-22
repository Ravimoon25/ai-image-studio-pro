from google.genai import types
from config.config import get_client, MODEL_ID
import io
import PIL.Image

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
