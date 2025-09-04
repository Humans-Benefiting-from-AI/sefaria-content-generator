from flask import Blueprint, request, jsonify
from src.sefaria_integration import SefariaAPIClient, SefariaContentGenerator

sefaria_bp = Blueprint("sefaria_bp", __name__)

sefaria_client = SefariaAPIClient()
basic_generator = SefariaContentGenerator(sefaria_client)

@sefaria_bp.route("/text")
def get_text():
    ref = request.args.get("ref")
    if not ref:
        return jsonify({"error": "Missing reference"}), 400
    try:
        text = sefaria_client.get_text(ref)
        return jsonify(text.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sefaria_bp.route("/generate")
def generate_content():
    content_type = request.args.get("type")
    ref = request.args.get("ref")

    if not content_type or not ref:
        return jsonify({"error": "Missing content type or reference"}), 400

    try:
        if content_type == "study_guide":
            content = basic_generator.generate_study_guide(ref)
        elif content_type == "commentary_collection":
            content = basic_generator.generate_commentary_collection(ref)
        elif content_type == "thematic_collection":
            # For now, return the same as commentary collection
            content = basic_generator.generate_commentary_collection(ref)
        else:
            return jsonify({"error": "Invalid content type"}), 400
        return jsonify(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

