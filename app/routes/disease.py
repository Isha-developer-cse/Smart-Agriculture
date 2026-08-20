from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, request

from ..extensions import db
from ..ml.disease_model import DiseaseClassifier
from ..models.prediction import DiseasePrediction


disease_bp = Blueprint("disease", __name__)
classifier = None


def get_classifier():
    global classifier
    if classifier is None:
        classifier = DiseaseClassifier(current_app.config["DISEASE_MODEL_PATH"])
    return classifier


@disease_bp.post("/predict-disease")
def predict_disease():
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "image file is required"}), 400

    current_app.config["UPLOAD_DIR"].mkdir(parents=True, exist_ok=True)
    extension = Path(image.filename).suffix.lower() or ".jpg"
    filename = f"{uuid4().hex}{extension}"
    image_path = current_app.config["UPLOAD_DIR"] / filename
    image.save(image_path)

    prediction = get_classifier().predict(image_path)
    row = DiseasePrediction(
        filename=filename,
        disease_name=prediction["disease_name"],
        confidence=prediction["confidence"],
        treatment="|".join(prediction["treatment"]),
        model_version=prediction["model_version"],
    )
    db.session.add(row)
    db.session.commit()

    response = row.to_dict()
    response["metrics"] = prediction.get("metrics", {})
    return jsonify(response)


@disease_bp.get("/predictions")
def predictions():
    rows = DiseasePrediction.query.order_by(DiseasePrediction.id.desc()).limit(20).all()
    return jsonify([row.to_dict() for row in rows])
