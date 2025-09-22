from google.genai import types
from config.config import get_client, MODEL_ID

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
            
            for part in response.parts:
                if hasattr(part, 'as_image') and part.as_image():
                    results.append(part.as_image())
                    break
        
        return results, "Images generated successfully!"
    except Exception as e:
        return [], f"Generation error: {str(e)}"
