from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db
from .models.user import User
from .models.prediction import DiseasePrediction
from .routes.auth import auth_bp
from .routes.crop import crop_bp, recommend_crop
from .routes.disease import disease_bp, predict_disease
from .routes.fertilizer import fertilizer_bp, fertilizer
from .routes.weather import weather_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(disease_bp, url_prefix="/api")
    app.register_blueprint(crop_bp, url_prefix="/api")
    app.register_blueprint(fertilizer_bp, url_prefix="/api")
    app.register_blueprint(weather_bp, url_prefix="/api")
    app.add_url_rule("/predict-disease", view_func=predict_disease, methods=["POST"])
    app.add_url_rule("/recommend-crop", view_func=recommend_crop, methods=["POST"])
    app.add_url_rule("/suggest-fertilizer", view_func=fertilizer, methods=["POST"])

    with app.app_context():
        db.create_all()

    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "smart-agro-backend"}

    return app
