import streamlit as st
from google import genai

# Model configuration
MODEL_ID = "gemini-import streamlit as st
from google import genai

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

def analyze_image_content(image, analysis_type):
    """Comprehensive image analysis and intelligence"""
    try:
        client = get_client()
        
        analysis_prompts = {
            "complete": """
            Provide comprehensive analysis of this image in the following structured format:
            
            CONTENT_ANALYSIS:
            - Objects: List all objects, people, animals visible
            - Scene_Type: Indoor/outdoor, location, environment
            - Activities: What people are doing, actions happening
            - Mood: Overall atmosphere and feeling
            
            TECHNICAL_QUALITY:
            - Resolution_Score: Rate image sharpness (1-10)
            - Lighting_Quality: Assess lighting quality (1-10) 
            - Composition_Score: Photography composition (1-10)
            - Color_Balance: Color accuracy and harmony (1-10)
            - Professional_Rating: Overall professional quality (1-10)
            
            PEOPLE_ANALYSIS:
            - Count: Number of people visible
            - Demographics: Age groups, gender distribution
            - Emotions: Facial expressions, mood analysis
            - Clothing: Outfit styles, formality level
            - Body_Language: Pose, confidence, energy
            
            BUSINESS_INTELLIGENCE:
            - Commercial_Value: Business usage potential (1-10)
            - Target_Audience: Who this appeals to
            - Marketing_Effectiveness: Social media potential (1-10)
            - Brand_Elements: Any logos, brands, products visible
            - Usage_Recommendations: Best platforms, contexts
            
            IMPROVEMENT_SUGGESTIONS:
            - Technical_Fixes: Specific quality improvements
            - Composition_Tips: Framing and layout suggestions  
            - Enhancement_Ideas: Creative improvement options
            
            KEYWORDS: 10 relevant tags for this image
            """,
            
            "text_extraction": """
            Extract and analyze ALL visible text in this image:
            
            EXTRACTED_TEXT:
            [Provide all visible text exactly as it appears, maintaining formatting]
            
            TEXT_ANALYSIS:
            - Language: Primary language(s) detected
            - Text_Type: (document, sign, handwritten, printed, display, etc.)
            - Structure: (paragraph, list, table, form, receipt, etc.)
            - Quality_Score: Text clarity and readability (1-10)
            - Business_Document_Type: (invoice, receipt, business card, form, etc.)
            
            STRUCTURED_DATA:
            [If receipt/invoice: extract line items, totals, dates]
            [If business card: extract name, phone, email, company]
            [If form: extract field names and values]
            [If table: organize data in rows and columns]
            
            KEYWORDS: Key terms and important phrases found
            SUMMARY: Brief description of text content
            
            If no text is visible, clearly state "NO TEXT DETECTED"
            """,
            
            "people_demographics": """
            Analyze all people in this image:
            
            PEOPLE_COUNT: Exact number of people visible
            
            DEMOGRAPHICS:
            - Age_Groups: Estimated age ranges for each person
            - Gender_Distribution: Gender breakdown
            - Ethnicity_Diversity: Cultural/ethnic representation
            
            FACIAL_ANALYSIS:
            - Expressions: Each person's facial expression
            - Emotions: Mood and emotional state
            - Eye_Contact: Where people are looking
            - Confidence_Level: Body language assessment
            
            CLOTHING_ANALYSIS:
            - Outfit_Styles: Describe each person's clothing
            - Formality_Level: Casual to formal rating (1-10)
            - Color_Coordination: How well outfits work together
            - Fashion_Era: Modern, vintage, traditional styling
            
            SOCIAL_DYNAMICS:
            - Group_Interaction: How people relate to each other
            - Professional_Suitability: Business usage appropriateness (1-10)
            - Social_Media_Ready: Instagram/LinkedIn readiness (1-10)
            """,
            
            "technical_quality": """
            Technical photography analysis:
            
            IMAGE_QUALITY:
            - Resolution: Image sharpness and detail (1-10)
            - Exposure: Brightness and contrast balance (1-10) 
            - Focus: Subject sharpness and depth (1-10)
            - Noise_Level: Grain and digital noise (1-10)
            
            COMPOSITION:
            - Rule_of_Thirds: Composition adherence (1-10)
            - Balance: Visual weight distribution (1-10)
            - Framing: Subject framing quality (1-10)
            - Leading_Lines: Use of visual guides (1-10)
            
            LIGHTING:
            - Lighting_Direction: Where light comes from
            - Lighting_Quality: Soft/hard light assessment (1-10)
            - Shadow_Detail: Shadow quality and placement (1-10)
            - Color_Temperature: Warm/cool light balance
            
            COLOR_ANALYSIS:
            - Color_Harmony: How colors work together (1-10)
            - Saturation: Color intensity appropriateness (1-10)
            - Contrast: Light/dark balance (1-10)
            - Dominant_Colors: Primary colors in image
            
            PROFESSIONAL_ASSESSMENT:
            - Commercial_Readiness: Ready for business use (1-10)
            - Improvement_Priority: What to fix first
            - Strengths: What's working well
            - Technical_Recommendations: Specific fixes needed
            """
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts["complete"])
        
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, image]
        )
        
        analysis_text = ""
        for part in response.parts:
            if part.text:
                analysis_text += part.text
        
        return analysis_text
        
    except Exception as e:
        return f"Analysis error: {str(e)}"
    """Comprehensive image analysis and intelligence"""
    try:
        client = get_client()
        
        analysis_prompts = {
            "complete": """
            Provide comprehensive analysis of this image in the following structured format:
            
            CONTENT_ANALYSIS:
            - Objects: List all objects, people, animals visible
            - Scene_Type: Indoor/outdoor, location, environment
            - Activities: What people are doing, actions happening
            - Mood: Overall atmosphere and feeling
            
            TECHNICAL_QUALITY:
            - Resolution_Score: Rate image sharpness (1-10)
            - Lighting_Quality: Assess lighting quality (1-10) 
            - Composition_Score: Photography composition (1-10)
            - Color_Balance: Color accuracy and harmony (1-10)
            - Professional_Rating: Overall professional quality (1-10)
            
            PEOPLE_ANALYSIS:
            - Count: Number of people visible
            - Demographics: Age groups, gender distribution
            - Emotions: Facial expressions, mood analysis
            - Clothing: Outfit styles, formality level
            - Body_Language: Pose, confidence, energy
            
            BUSINESS_INTELLIGENCE:
            - Commercial_Value: Business usage potential (1-10)
            - Target_Audience: Who this appeals to
            - Marketing_Effectiveness: Social media potential (1-10)
            - Brand_Elements: Any logos, brands, products visible
            - Usage_Recommendations: Best platforms, contexts
            
            IMPROVEMENT_SUGGESTIONS:
            - Technical_Fixes: Specific quality improvements
            - Composition_Tips: Framing and layout suggestions  
            - Enhancement_Ideas: Creative improvement options
            
            KEYWORDS: 10 relevant tags for this image
            """,
            
            "text_extraction": """
            Extract and analyze ALL visible text in this image:
            
            EXTRACTED_TEXT:
            [Provide all visible text exactly as it appears, maintaining formatting]
            
            TEXT_ANALYSIS:
            - Language: Primary language(s) detected
            - Text_Type: (document, sign, handwritten, printed, display, etc.)
            - Structure: (paragraph, list, table, form, receipt, etc.)
            - Quality_Score: Text clarity and readability (1-10)
            - Business_Document_Type: (invoice, receipt, business card, form, etc.)
            
            STRUCTURED_DATA:
            [If receipt/invoice: extract line items, totals, dates]
            [If business card: extract name, phone, email, company]
            [If form: extract field names and values]
            [If table: organize data in rows and columns]
            
            KEYWORDS: Key terms and important phrases found
            SUMMARY: Brief description of text content
            
            If no text is visible, clearly state "NO TEXT DETECTED"
            """,
            
            "people_demographics": """
            Analyze all people in this image:
            
            PEOPLE_COUNT: Exact number of people visible
            
            DEMOGRAPHICS:
            - Age_Groups: Estimated age ranges for each person
            - Gender_Distribution: Gender breakdown
            - Ethnicity_Diversity: Cultural/ethnic representation
            
            FACIAL_ANALYSIS:
            - Expressions: Each person's facial expression
            - Emotions: Mood and emotional state
            - Eye_Contact: Where people are looking
            - Confidence_Level: Body language assessment
            
            CLOTHING_ANALYSIS:
            - Outfit_Styles: Describe each person's clothing
            - Formality_Level: Casual to formal rating (1-10)
            - Color_Coordination: How well outfits work together
            - Fashion_Era: Modern, vintage, traditional styling
            
            SOCIAL_DYNAMICS:
            - Group_Interaction: How people relate to each other
            - Professional_Suitability: Business usage appropriateness (1-10)
            - Social_Media_Ready: Instagram/LinkedIn readiness (1-10)
            """,
            
            "technical_quality": """
            Technical photography analysis:
            
            IMAGE_QUALITY:
            - Resolution: Image sharpness and detail (1-10)
            - Exposure: Brightness and contrast balance (1-10) 
            - Focus: Subject sharpness and depth (1-10)
            - Noise_Level: Grain and digital noise (1-10)
            
            COMPOSITION:
            - Rule_of_Thirds: Composition adherence (1-10)
            - Balance: Visual weight distribution (1-10)
            - Framing: Subject framing quality (1-10)
            - Leading_Lines: Use of visual guides (1-10)
            
            LIGHTING:
            - Lighting_Direction: Where light comes from
            - Lighting_Quality: Soft/hard light assessment (1-10)
            - Shadow_Detail: Shadow quality and placement (1-10)
            - Color_Temperature: Warm/cool light balance
            
            COLOR_ANALYSIS:
            - Color_Harmony: How colors work together (1-10)
            - Saturation: Color intensity appropriateness (1-10)
            - Contrast: Light/dark balance (1-10)
            - Dominant_Colors: Primary colors in image
            
            PROFESSIONAL_ASSESSMENT:
            - Commercial_Readiness: Ready for business use (1-10)
            - Improvement_Priority: What to fix first
            - Strengths: What's working well
            - Technical_Recommendations: Specific fixes needed
            """
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts["complete"])
        
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, image]
        )
        
        analysis_text = ""
        for part in response.parts:
            if part.text:
                analysis_text += part.text
        
        return analysis_text
        
    except Exception as e:
        return f"Analysis error: {str(e)}"
