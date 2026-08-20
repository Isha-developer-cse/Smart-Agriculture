import joblib
import numpy as np


class CropRecommender:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = joblib.load(model_path) if model_path.exists() else None
        self.labels = ["rice", "maize", "chickpea", "kidneybeans", "cotton", "mango", "grapes", "watermelon"]

    def recommend(self, payload):
        features = np.array(
            [
                [
                    float(payload["nitrogen"]),
                    float(payload["phosphorus"]),
                    float(payload["potassium"]),
                    float(payload["temperature"]),
                    float(payload["humidity"]),
                    float(payload["ph"]),
                    float(payload["rainfall"]),
                ]
            ]
        )

        if self.model:
            crop = self.model.predict(features)[0]
            probabilities = getattr(self.model, "predict_proba", lambda _: None)(features)
            confidence = float(np.max(probabilities)) if probabilities is not None else 0.86
            return {"crop": str(crop), "confidence": round(confidence, 4), "model_version": "random-forest"}

        nitrogen, _, potassium, temperature, humidity, ph, rainfall = features[0]
        if rainfall > 180 and humidity > 65:
            crop = "rice"
        elif temperature > 28 and potassium > 35:
            crop = "cotton"
        elif 5.5 <= ph <= 7.5 and nitrogen > 45:
            crop = "mango"
        elif rainfall < 90:
            crop = "maize"
        else:
            crop = "chickpea"
        return {"crop": crop, "confidence": 0.74, "model_version": "rule-fallback"}
