# AI Image Studio Pro

A comprehensive AI-powered image generation, editing, and analysis platform built with Streamlit and Google Gemini AI.

## Features

### 🎭 Image Generation
- Text-to-image generation with advanced prompting
- Multiple art styles and aspect ratios
- Batch generation capabilities
- Quality enhancement options
- Template library with 50+ professional prompts

### ✏️ Image Editing & Transformation
- **Face Swap**: Advanced face swapping between images
- **Outfit Changes**: Transform clothing and styling
- **Pose & Expression**: Modify body language and facial expressions
- **Face Enhancement**: Professional beauty and skin improvements
- **Body Modification**: Fitness and body shape adjustments
- **Background Control**: Replace, remove, or enhance backgrounds
- **Object Management**: Add, remove, or modify objects
- **Complete Makeovers**: Full appearance transformations
- **Style Transfer**: Apply artistic styles

### 🔍 Analysis & Intelligence
- **OCR Text Extraction**: Extract and analyze text from images
- **People Demographics**: Analyze age, gender, emotions, clothing
- **Technical Quality**: Assess image quality, composition, lighting
- **Business Intelligence**: Marketing potential and commercial value
- **Content Safety**: Automated content moderation

### 💡 Professional Features
- **Batch Processing**: Handle multiple images simultaneously
- **Usage Analytics**: Track and analyze usage patterns
- **Export Options**: Multiple format support (PNG, JPEG, JSON, TXT)
- **History Management**: Save and revisit past operations
- **Mobile Optimization**: Responsive design for all devices

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-image-studio-pro.git
cd ai-image-studio-pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .streamlit/secrets.toml file
mkdir .streamlit
echo 'GOOGLE_API_KEY = "your-google-api-key"' > .streamlit/secrets.toml
```

4. Run the application:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Fork this repository
2. Connect your GitHub account to Streamlit Cloud
3. Deploy the app by selecting this repository
4. Add your Google API key in the Secrets management:
   ```
   GOOGLE_API_KEY = "your-google-api-key"
   ```

## Configuration

### Google API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Add the API key to your Streamlit secrets

### Model Configuration

The app uses the `gemini-2.5-flash-image-preview` model. You can modify the model in `config/config.py` if needed.

## Project Structure

```
ai-image-studio-pro/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── config/
│   └── config.py         # Configuration and constants
├── services/
│   ├── generation_service.py    # Image generation logic
│   ├── editing_service.py       # Image editing logic
│   └── analysis_service.py      # Image analysis logic
├── components/
│   ├── generation_tab.py        # Generation UI component
│   ├── editing_tab.py           # Editing UI component
│   ├── analysis_tab.py          # Analysis UI component
│   ├── history_tab.py           # History UI component
│   ├── pro_features_tab.py      # Pro features UI component
│   └── sidebar.py               # Sidebar component
└── utils/
    └── utils.py                 # Utility functions
```

## Usage

### Image Generation
1. Navigate to the "Generate" tab
2. Enter a detailed description of your desired image
3. Select style, aspect ratio, and other options
4. Click "Generate Images"

### Image Editing
1. Go to the "Edit & Transform" tab
2. Upload an image
3. Choose transformation type (Face Swap, Outfit Change, etc.)
4. Configure options and click the transform button

### Image Analysis
1. Visit the "Analyze & Extract" tab
2. Upload an image
3. Select analysis type (OCR, Demographics, Quality, etc.)
4. Click "Analyze Image"

## Features in Detail

### Advanced Face Swap
- Natural skin tone matching
- Lighting adjustment
- Hair preservation options
- High-quality blending

### Professional Enhancement
- Skin smoothing and blemish removal
- Eye brightening and enhancement
- Smile improvement
- Body fitness modifications

### Batch Operations
- Generate multiple images from different prompts
- Analyze multiple images simultaneously
- Export batch results

### Analytics Dashboard
- Track usage statistics
- Monitor feature adoption
- Export usage reports

## API Limits

- Google Gemini API has usage quotas
- Monitor your usage in Google Cloud Console
- The app includes usage tracking and warnings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Changelog

### v1.0.0
- Initial release
- 68+ professional features
- Complete modular architecture
- Mobile-optimized responsive design
- Comprehensive image processing capabilities
