from flask import Blueprint, jsonify, request

from ..services.fertilizer_service import suggest_fertilizer


fertilizer_bp = Blueprint("fertilizer", __name__)


@fertilizer_bp.post("/suggest-fertilizer")
def fertilizer():
    payload = request.get_json() or {}
    required = ["nitrogen", "phosphorus", "potassium", "crop"]
    missing = [field for field in required if field not in payload]
    if missing:
        return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400
    return jsonify(suggest_fertilizer(payload))
