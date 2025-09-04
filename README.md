# Sefaria Content Generator 🕎

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Sefaria API](https://img.shields.io/badge/Sefaria-API-blue.svg)](https://developers.sefaria.org/)

A comprehensive tool for creating Jewish educational content using the Sefaria API, including Torah study guides, holiday materials, and calendar-based content.

> **🎯 Purpose**: Empowering educators, rabbis, and students to create rich Jewish educational materials by leveraging the vast digital library of Sefaria.

## Project Structure

```
sefaria-content-generator/
├── src/
│   ├── core/                 # Core functionality modules
│   │   ├── sefaria_integration.py    # Main Sefaria API integration
│   │   ├── torah_api.py              # Torah-specific API functions
│   │   └── jewish_calendar.py        # Jewish calendar calculations
│   ├── generators/           # Content generation modules
│   │   ├── advanced_content_generator.py
│   │   ├── holiday_content_generator.py
│   │   ├── torah_content_generator.py
│   │   └── content_templates.py
│   └── api/                  # API routes and endpoints
│       ├── sefaria_api_routes.py
│       └── sefaria_api_routes_simple.py
├── web/                      # Web interface
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── docs/                     # Documentation
├── tests/                    # Test files and results
├── examples/                 # Example usage and output
├── main.py                   # Main application entry point
├── main_simple.py           # Simplified application version
├── minimal_app.py           # Minimal demo application
└── requirements.txt         # Python dependencies
```

## Features

- **Torah Content Generation**: Create study guides, commentary, and educational materials
- **Holiday Content**: Generate content for Jewish holidays and celebrations
- **Calendar Integration**: Jewish calendar calculations and date-based content
- **Web Interface**: User-friendly web application for content creation
- **API Integration**: Comprehensive Sefaria API integration
- **Template System**: Flexible content templates for different formats

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sefaria-content-generator.git
   cd sefaria-content-generator
   ```

2. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install flask-cors
   ```

4. **Run the application**:
   ```bash
   python main_working.py
   ```

5. **Access the web interface**:
   Open your browser to `http://localhost:8080`

### Alternative Setup

If you're setting up for development or want to push to your own GitHub repository, use the automated setup script:

```bash
chmod +x setup_github.sh
./setup_github.sh
```

## Documentation

See the `docs/` directory for detailed documentation including:
- Sefaria API integration guide
- Jewish calendar research
- Torah content generation examples
- Task progress and development notes

## Testing

Run the comprehensive test suite:
```bash
python tests/comprehensive_test_suite.py
```

## Contributing

This project helps create educational Jewish content using the rich resources available through the Sefaria API.

## 🤝 Contributing

We welcome contributions from the Jewish educational technology community! Whether you're a developer, educator, or Jewish studies enthusiast, your input is valuable.

- **🐛 Found a bug?** [Open an issue](https://github.com/YOUR_USERNAME/sefaria-content-generator/issues)
- **💡 Have an idea?** [Start a discussion](https://github.com/YOUR_USERNAME/sefaria-content-generator/discussions)
- **🔧 Want to contribute code?** Check out [CONTRIBUTING.md](CONTRIBUTING.md)

## 📊 Project Status

This project is actively maintained and welcomes community contributions. Key areas for development:

- [ ] Enhanced error handling for API failures
- [ ] Additional content templates and formats
- [ ] User authentication and saved content
- [ ] Export functionality (PDF, Word, etc.)
- [ ] Mobile-responsive interface improvements

## 🙏 Acknowledgments

- **[Sefaria](https://www.sefaria.org)** for providing the comprehensive Jewish texts API
- **Jewish educational technology community** for inspiration and feedback
- **Open source contributors** who help make this tool better

## 📞 Support

- **Documentation**: Check the `docs/` folder and README
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Community**: Join discussions for questions and ideas

## 🏷️ Topics

`sefaria` `jewish-texts` `torah` `education` `content-generation` `flask` `python` `api` `jewish-studies` `educational-technology`