from datetime import datetime, timezone

from ..extensions import db


class DiseasePrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    disease_name = db.Column(db.String(160), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    model_version = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "disease_name": self.disease_name,
            "confidence": round(self.confidence, 4),
            "treatment": self.treatment.split("|"),
            "model_version": self.model_version,
            "created_at": self.created_at.isoformat(),
        }
