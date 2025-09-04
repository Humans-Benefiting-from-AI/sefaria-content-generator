# Contributing to Sefaria Content Generator

Thank you for your interest in contributing to the Sefaria Content Generator! This project aims to make Jewish educational content creation more accessible and efficient.

## 🕎 About the Project

The Sefaria Content Generator is a comprehensive tool for creating Jewish educational content using the Sefaria API. It enables educators, rabbis, and students to generate study guides, commentary collections, and thematic content based on traditional Jewish texts.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/YOUR_USERNAME/sefaria-content-generator/issues) section
2. If not, create a new issue with:
   - Clear description of the problem or feature
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment details

### Code Contributions

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/sefaria-content-generator.git
   cd sefaria-content-generator
   ```

3. **Set up development environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install flask-cors
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes**:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

6. **Test your changes**:
   ```bash
   python main_working.py
   # Test the web interface at http://localhost:8080
   
   # Run tests if available
   python tests/comprehensive_test_suite.py
   ```

7. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

8. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and single-purpose

### File Organization

```
src/
├── core/          # Core Sefaria API integration
├── generators/    # Content generation modules
├── api/          # Flask API routes
web/
├── templates/    # HTML templates
├── static/       # CSS, JS, images
docs/            # Documentation
tests/           # Test files
```

### Testing

- Add tests for new features
- Ensure existing tests pass
- Test with various Sefaria references
- Verify web interface functionality

### Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Update API documentation if adding endpoints

## 🎯 Areas for Contribution

### High Priority
- **Enhanced error handling** for API failures
- **Additional content templates** for different formats
- **User authentication system** for saved content
- **Export functionality** (PDF, Word, etc.)

### Medium Priority
- **Mobile-responsive web interface**
- **Advanced search functionality**
- **Content collaboration features**
- **Internationalization support**

### Low Priority
- **Integration with other Jewish text APIs**
- **Machine learning for content recommendations**
- **Advanced analytics dashboard**

## 🔧 Technical Details

### Key Dependencies
- **Flask**: Web framework
- **Requests**: HTTP library for Sefaria API
- **Dataclasses**: For structured data handling

### API Endpoints
- `GET /api/text?ref=<reference>` - Fetch text from Sefaria
- `GET /api/generate?type=<type>&ref=<reference>` - Generate content
- `GET /api/templates` - List available templates
- `GET /api/health` - Health check

### Sefaria API Integration
The tool integrates with the [Sefaria API](https://developers.sefaria.org/) to:
- Retrieve Jewish texts in Hebrew and English
- Access commentary and related materials
- Fetch metadata and source information

## 🙏 Recognition

Contributors will be recognized in:
- Repository contributors list
- Release notes for their contributions
- Special mentions for significant improvements

## 📞 Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For general questions and ideas
- **Email**: Contact the maintainers for sensitive issues

## 📜 Code of Conduct

This project follows a code of conduct that encourages:
- Respectful and inclusive communication
- Constructive feedback and collaboration
- Recognition of diverse backgrounds and perspectives
- Educational focus aligned with Jewish values

Thank you for helping make Jewish educational content more accessible to everyone! 🕎