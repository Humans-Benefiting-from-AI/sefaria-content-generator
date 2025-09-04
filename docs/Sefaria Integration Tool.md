# Sefaria Integration Tool

A comprehensive web-based tool for integrating with the Sefaria API to fetch Jewish texts and sources, and generate educational content based on them.

## Features

### Core Functionality
- **Text Retrieval**: Fetch any text from the Sefaria library using standard references (e.g., "Genesis 1:1")
- **Content Generation**: Create study guides, commentary collections, and thematic collections
- **AI-Enhanced Analysis**: Generate insights and educational content using OpenAI integration
- **Web Interface**: User-friendly interface for easy interaction with the tool

### Supported Content Types
1. **Study Guides**: Comprehensive guides with context, questions, and analysis
2. **Commentary Collections**: Curated collections of traditional commentaries
3. **Thematic Collections**: Content organized around specific themes or topics

## Installation

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)
- Internet connection for API access

### Setup
1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd sefaria-tool-ui
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install flask requests openai
   ```
5. Set up environment variables (optional):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export OPENAI_API_BASE="your-openai-api-base"
   ```

## Usage

### Starting the Application
1. Activate your virtual environment
2. Run the Flask application:
   ```bash
   python src/main.py
   ```
3. Open your browser and navigate to `http://localhost:5000`

### Using the Web Interface

#### Text Retrieval
1. Enter a Sefaria reference in the "Text Retrieval" section (e.g., "Genesis 1:1", "Mishnah Avot 1:1")
2. Click "Fetch Text" to retrieve the text and metadata
3. The response will include the original text, language, version information, and source details

#### Content Generation
1. Select the type of content you want to generate:
   - **Study Guide**: Comprehensive educational material
   - **Commentary Collection**: Traditional commentaries and interpretations
   - **Thematic Collection**: Content organized around themes
2. Enter a reference or theme in the input field
3. Click "Generate Content" to create the content
4. The generated content will appear below with structured information

## API Endpoints

### Text Retrieval
- **Endpoint**: `GET /api/text`
- **Parameters**: 
  - `ref` (required): Sefaria text reference
- **Example**: `/api/text?ref=Genesis%201:1`

### Content Generation
- **Endpoint**: `GET /api/generate`
- **Parameters**:
  - `type` (required): Content type (`study_guide`, `commentary_collection`, `thematic_collection`)
  - `ref` (required): Text reference or theme
- **Example**: `/api/generate?type=study_guide&ref=Genesis%201:1`

## Architecture

### Core Components

#### 1. SefariaAPIClient (`sefaria_integration.py`)
- Handles all interactions with the Sefaria API
- Provides methods for text retrieval, related content, and search
- Implements rate limiting and error handling

#### 2. Content Generators
- **SefariaContentGenerator**: Basic content generation (commentary collections, study guides)
- **AdvancedContentGenerator**: AI-enhanced content generation with OpenAI integration

#### 3. Flask Web Application (`main.py`)
- Serves the web interface
- Provides REST API endpoints
- Handles routing and static file serving

#### 4. Frontend Interface
- **HTML**: Clean, responsive interface (`static/index.html`)
- **CSS**: Modern styling with dark theme (`static/style.css`)
- **JavaScript**: Interactive functionality and API communication (`static/script.js`)

### Data Models

#### SefariaText
```python
@dataclass
class SefariaText:
    ref: str
    text: Union[str, List[str]]
    language: str
    version_title: str
    version_source: str
    license: str
    priority: int
    status: str
    format_as_poetry: bool = False
```

#### SefariaRelated
```python
@dataclass
class SefariaRelated:
    ref: str
    links: List[Dict[str, Any]]
    sheets: List[Dict[str, Any]]
    notes: List[Dict[str, Any]]
    media: List[Dict[str, Any]]
    topics: List[Dict[str, Any]]
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI-enhanced features
- `OPENAI_API_BASE`: OpenAI API base URL (optional)

### Rate Limiting
The tool implements rate limiting for Sefaria API calls (default: 0.1 seconds between requests). This can be adjusted in the `SefariaAPIClient` initialization.

## Examples

### Basic Text Retrieval
```python
from sefaria_integration import SefariaAPIClient

client = SefariaAPIClient()
text = client.get_text("Genesis 1:1")
print(text.get_text_content())
```

### Generating a Study Guide
```python
from sefaria_integration import SefariaAPIClient, SefariaContentGenerator

client = SefariaAPIClient()
generator = SefariaContentGenerator(client)
study_guide = generator.generate_study_guide("Genesis 1:1")
print(study_guide['study_questions'])
```

### Advanced Content Generation
```python
from advanced_content_generator import AdvancedContentGenerator

advanced_gen = AdvancedContentGenerator(client)
comprehensive_guide = advanced_gen.create_comprehensive_study_guide("Genesis 1:1")
```

## Testing

The tool includes comprehensive test suites:

1. **API Integration Tests**: Test Sefaria API connectivity and data retrieval
2. **Content Generation Tests**: Verify content generation functionality
3. **Web Interface Tests**: Test the Flask application and endpoints

Run tests with:
```bash
python comprehensive_test_suite.py
```

## Deployment

### Local Development
The tool runs on `localhost:5000` by default for development.

### Production Deployment
For production deployment:
1. Set `debug=False` in the Flask app configuration
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper environment variables
4. Ensure CORS is properly configured for your domain

### Docker Deployment (Optional)
A Dockerfile can be created for containerized deployment:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "src/main.py"]
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check internet connectivity
   - Verify Sefaria API is accessible
   - Check for rate limiting issues

2. **OpenAI Integration Issues**
   - Ensure `OPENAI_API_KEY` is set correctly
   - Verify API quota and billing status
   - Check model availability

3. **Flask Application Issues**
   - Ensure all dependencies are installed
   - Check port availability (5000)
   - Verify file permissions

### Debug Mode
Enable debug mode for development:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for all functions and classes
- Include error handling and logging

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **Sefaria**: For providing the comprehensive Jewish text API
- **OpenAI**: For AI-powered content generation capabilities
- **Flask**: For the web framework
- **Community**: For feedback and contributions

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section
2. Review existing issues
3. Create a new issue with detailed information
4. Contact the development team

---

**Version**: 1.0  
**Last Updated**: September 2025  
**Author**: Manus AI Assistant

