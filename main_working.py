import logging
#!/usr/bin/env python3
"""
Working Sefaria Content Generator Application

A Flask application for creating Jewish educational content using the Sefaria API.
This version fixes the import issues and provides a working web interface.
"""

import os
import sys
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the core Sefaria integration module
try:
    from src.core.sefaria_integration import SefariaAPIClient, SefariaText
    from src.generators.advanced_content_generator import AdvancedContentGenerator
    from src.generators.content_templates import ContentTemplates
    SEFARIA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Sefaria modules not available: {e}")
    SEFARIA_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sefaria-content-generator-key-2024'

# Enable CORS for development
CORS(app)

# Configure static and template folders
app.static_folder = os.path.join(os.path.dirname(__file__), 'web', 'static')
app.template_folder = os.path.join(os.path.dirname(__file__), 'web', 'templates')

# Initialize Sefaria client if available
if SEFARIA_AVAILABLE:
    try:
        sefaria_client = SefariaAPIClient()
        content_generator = AdvancedContentGenerator(sefaria_client)
        templates = ContentTemplates()
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        print(f"Error initializing Sefaria client: {e}")
        SEFARIA_AVAILABLE = False

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/text')
def get_text():
    """Fetch text from Sefaria API"""
    if not SEFARIA_AVAILABLE:
        return jsonify({"error": "Sefaria integration not available"}), 503
    
    ref = request.args.get('ref')
    if not ref:
        return jsonify({"error": "Missing reference parameter"}), 400
    
    try:
        text_obj = sefaria_client.get_text(ref)
        return jsonify({
            "ref": text_obj.ref,
            "text": text_obj.get_text_content(),
            "language": text_obj.language,
            "version_title": text_obj.version_title,
            "success": True
        })
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({"error": "Internal server error", "success": False}), 500

@app.route('/api/generate')
def generate_content():
    """Generate various types of Jewish educational content"""
    if not SEFARIA_AVAILABLE:
        return jsonify({"error": "Sefaria integration not available"}), 503
    
    content_type = request.args.get('type')
    ref = request.args.get('ref')
    
    if not content_type or not ref:
        return jsonify({"error": "Missing content type or reference"}), 400
    
    try:
        if content_type == "study_guide":
            content = content_generator.create_comprehensive_study_guide(ref)
        elif content_type == "commentary_collection":
            content = content_generator.generate_commentary_collection(ref)
        elif content_type == "thematic_collection":
            content = content_generator.create_thematic_collection(ref)
        else:
            return jsonify({"error": "Invalid content type"}), 400
            
        return jsonify({
            "content": content,
            "type": content_type,
            "reference": ref,
            "success": True
        })
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({"error": "Internal server error", "success": False}), 500

@app.route('/api/templates')
def get_templates():
    """Get available content templates"""
    if not SEFARIA_AVAILABLE:
        return jsonify({"error": "Sefaria integration not available"}), 503
    
    try:
        available_templates = {
            "study_guide": "Comprehensive study guide with questions and analysis",
            "commentary_collection": "Collection of traditional commentaries",
            "thematic_collection": "Thematically organized content",
            "holiday_content": "Holiday-specific educational materials",
            "torah_portion": "Weekly Torah portion study materials"
        }
        return jsonify({
            "templates": available_templates,
            "success": True
        })
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({"error": "Internal server error", "success": False}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "sefaria_integration": SEFARIA_AVAILABLE,
        "version": "1.0.0"
    }
    return jsonify(status)

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🕎 Starting Sefaria Content Generator")
    print(f"📁 Template folder: {app.template_folder}")
    print(f"📂 Static folder: {app.static_folder}")
    print(f"🔗 Sefaria integration: {'✅ Available' if SEFARIA_AVAILABLE else '❌ Not available'}")
    print("🌐 Server starting at http://localhost:8080")
    
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    )