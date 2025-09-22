# Deployment Guide

## Streamlit Cloud Deployment (Recommended)

### Prerequisites
1. GitHub account
2. Google API key from [Google AI Studio](https://aistudio.google.com/)

### Steps
1. **Fork the Repository**
   - Fork this repository to your GitHub account

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"

3. **Configure Deployment**
   - Repository: Select your forked repository
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: Choose a custom URL (optional)

4. **Add Secrets**
   - In the "Advanced settings" section
   - Add the following in the secrets section:
   ```toml
   GOOGLE_API_KEY = "your-actual-api-key-here"
   ```

5. **Deploy**
   - Click "Deploy!"
   - Wait for deployment to complete

### Post-Deployment
- Your app will be available at the provided URL
- Automatic updates when you push to the main branch
- Monitor usage through Streamlit Cloud dashboard

## Local Development

### Setup
1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create secrets file:
   ```bash
   mkdir .streamlit
   echo 'GOOGLE_API_KEY = "your-api-key"' > .streamlit/secrets.toml
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Alternative Deployment Options

### Heroku
1. Create a `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]" > ~/.streamlit/config.toml
   echo "port = $PORT" >> ~/.streamlit/config.toml
   echo "enableCORS = false" >> ~/.streamlit/config.toml
   echo "headless = true" >> ~/.streamlit/config.toml
   ```
3. Set environment variable: `GOOGLE_API_KEY`

### Google Cloud Run
1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8080
   CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```
2. Build and deploy using Cloud Run

### AWS EC2
1. Launch EC2 instance
2. Install Python and dependencies
3. Configure security groups (port 8501)
4. Use systemd for process management

## Environment Variables

Required:
- `GOOGLE_API_KEY`: Your Google Gemini API key

Optional:
- `MODEL_ID`: Override default model (default: gemini-2.5-flash-image-preview)

## Security Considerations

1. **Never commit API keys** to version control
2. Use **secrets management** for production deployments
3. **Monitor API usage** to prevent unexpected charges
4. **Set up alerts** for unusual activity
5. **Use HTTPS** in production

## Performance Optimization

1. **Enable caching** for expensive operations
2. **Optimize images** before processing
3. **Monitor memory usage** with large images
4. **Set request timeouts** appropriately
5. **Use CDN** for static assets if needed

## Monitoring

1. **Streamlit Cloud**: Built-in analytics
2. **Google Cloud Console**: API usage monitoring
3. **Custom logging**: Add application-level logging
4. **Error tracking**: Implement error reporting

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Verify API key is correct
   - Check if API is enabled in Google Cloud Console
   - Ensure billing is set up

2. **Memory Issues**
   - Reduce image sizes
   - Implement image compression
   - Use streaming for large files

3. **Timeout Errors**
   - Increase timeout settings
   - Implement retry logic
   - Use async processing for long operations

4. **Import Errors**
   - Check requirements.txt is complete
   - Verify Python version compatibility
   - Clear cache and reinstall dependencies

### Performance Issues
- Monitor API quotas
- Optimize prompt engineering
- Implement result caching
- Use batch processing for multiple operations

## Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Monitor for security patches
   - Update API models when available

2. **Backup Strategy**
   - Regular code backups
   - Export user data periodically
   - Document configuration changes

3. **Monitoring**
   - Set up health checks
   - Monitor error rates
   - Track user engagement metrics
