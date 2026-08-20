from flask import Blueprint, current_app, jsonify, request

from ..services.crop_service import CropRecommender


crop_bp = Blueprint("crop", __name__)
recommender = None


def get_recommender():
    global recommender
    if recommender is None:
        recommender = CropRecommender(current_app.config["CROP_MODEL_PATH"])
    return recommender


@crop_bp.post("/recommend-crop")
def recommend_crop():
    payload = request.get_json() or {}
    required = ["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph", "rainfall"]
    missing = [field for field in required if field not in payload]
    if missing:
        return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400
    return jsonify(get_recommender().recommend(payload))
