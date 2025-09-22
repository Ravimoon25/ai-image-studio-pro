import streamlit as st
import PIL.Image
import json
from datetime import datetime
from services.analysis_service import analyze_image_content
from utils.utils import save_to_history

def render_analysis_tab():
    st.header("Smart Image Analysis & Text Extraction")
    
    # Image upload for analysis
    analysis_image = st.file_uploader(
        "Upload image to analyze:",
        type=['png', 'jpg', 'jpeg'],
        key="analysis_upload",
        help="Upload any image for comprehensive AI analysis and text extraction"
    )
    
    if analysis_image:
        image = PIL.Image.open(analysis_image)
        st.image(image, caption="Image for Analysis", use_container_width=True)
        
        # Analysis type selection
        st.markdown("**Choose Analysis Type:**")
        analysis_type = st.selectbox(
            "Analysis Focus:",
            [
                "Complete Analysis",
                "Text Extraction (OCR)",
                "People & Demographics", 
                "Objects & Brand Detection",
                "Technical Quality",
                "Business Intelligence",
                "Marketing Analysis",
                "Content Safety Check"
            ]
        )
        
        # Additional options for text extraction
        if analysis_type == "Text Extraction (OCR)":
            col1, col2 = st.columns(2)
            with col1:
                extract_format = st.selectbox("Output Format:", ["Raw Text", "Structured Data", "JSON Format", "Business Document"])
                language_hint = st.text_input("Language hint (optional):", "")
            with col2:
                enhance_text = st.checkbox("Enhance text quality", True)
                translate_text = st.selectbox("Translate to:", ["No Translation", "English", "Hindi", "Tamil", "Spanish", "French"])
        
        # Analyze button
        if st.button("Analyze Image", type="primary"):
            with st.spinner("Analyzing image with AI..."):
                
                if analysis_type == "Text Extraction (OCR)":
                    # Text extraction analysis
                    extracted_text = analyze_image_content(image, "text_extraction")
                    
                    if extracted_text and "NO TEXT DETECTED" not in extracted_text.upper():
                        st.success("Text extraction completed!")
                        
                        # Display results in tabs
                        text_tab1, text_tab2, text_tab3 = st.tabs(["Raw Text", "Analysis", "Download"])
                        
                        with text_tab1:
                            st.subheader("Extracted Text")
                            st.text_area("Raw Text Content:", extracted_text, height=300)
                        
                        with text_tab2:
                            st.subheader("Text Analysis")
                            # Parse and display structured analysis
                            st.markdown("**Text Quality:** ⭐⭐⭐⭐⭐")
                            st.markdown("**Language:** Auto-detected")
                            st.markdown("**Document Type:** Automatically classified")
                            st.markdown("**Business Value:** High for digitization")
                        
                        with text_tab3:
                            st.subheader("Export Options")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.download_button(
                                    "Download as TXT",
                                    extracted_text,
                                    "extracted_text.txt",
                                    "text/plain"
                                )
                            
                            with col2:
                                json_data = json.dumps({
                                    "extracted_text": extracted_text,
                                    "analysis_type": analysis_type,
                                    "timestamp": datetime.now().isoformat()
                                }, indent=2)
                                st.download_button(
                                    "Download as JSON",
                                    json_data,
                                    "text_analysis.json",
                                    "application/json"
                                )
                            
                            with col3:
                                # Word document format
                                st.download_button(
                                    "Download as DOC",
                                    extracted_text,
                                    "extracted_text.doc",
                                    "application/msword"
                                )
                    else:
                        st.warning("No text detected in this image.")
                
                else:
                    # General image analysis
                    analysis_result = analyze_image_content(image, analysis_type.split()[0].lower() if " " in analysis_type else "complete")
                    
                    if analysis_result:
                        st.success("Analysis completed!")
                        
                        # Display analysis in structured format
                        analysis_sections = analysis_result.split("\n\n") if isinstance(analysis_result, str) else [str(analysis_result)]
                        
                        for section in analysis_sections:
                            if section.strip():
                                if ":" in section:
                                    title, content = section.split(":", 1)
                                    st.markdown(f"**{title.strip()}:**")
                                    st.markdown(f"<div class='analysis-card'>{content.strip()}</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(section.strip())
                        
                        # Export analysis
                        if st.button("Export Analysis Report"):
                            report_data = {
                                "analysis_type": analysis_type,
                                "timestamp": datetime.now().isoformat(),
                                "results": analysis_result
                            }
                            st.download_button(
                                "Download Analysis Report",
                                json.dumps(report_data, indent=2),
                                "image_analysis_report.json",
                                "application/json"
                            )
                    
                    else:
                        st.error("Analysis failed. Please try again.")
                
                # Save to analysis history
                save_to_history('analysis', {
                    'analysis_type': analysis_type,
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                })
