import logging
from flask import Blueprint, request, jsonify
import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.core.sefaria_integration import SefariaAPIClient
from src.generators.advanced_content_generator import AdvancedContentGenerator

sefaria_bp = Blueprint("sefaria_bp", __name__)

try:
    sefaria_client = SefariaAPIClient()
    advanced_generator = AdvancedContentGenerator(sefaria_client)
except Exception as e:
    logging.getLogger(__name__).exception("Request failed")
    sefaria_client = None
    advanced_generator = None
    print(f"Warning: Could not initialize Sefaria components: {e}")

@sefaria_bp.route("/text")
def get_text():
    ref = request.args.get("ref")
    if not ref:
        return jsonify({"error": "Missing reference"}), 400
    try:
        text = sefaria_client.get_text(ref)
        return jsonify(text.to_dict())
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({"error": "Internal server error"}), 500

@sefaria_bp.route("/generate")
def generate_content():
    content_type = request.args.get("type")
    ref = request.args.get("ref")

    if not content_type or not ref:
        return jsonify({"error": "Missing content type or reference"}), 400

    try:
        if content_type == "study_guide":
            content = advanced_generator.create_comprehensive_study_guide(ref)
        elif content_type == "commentary_collection":
            content = advanced_generator.basic_generator.generate_commentary_collection(ref)
        elif content_type == "thematic_collection":
            content = advanced_generator.create_thematic_collection(ref)
        else:
            return jsonify({"error": "Invalid content type"}), 400
        return jsonify(content)
    except Exception as e:
        logging.getLogger(__name__).exception("Request failed")
        return jsonify({"error": "Internal server error"}), 500


