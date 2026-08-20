import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'instance' / 'smart_agro.db').as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173").split(",")
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads"))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    DISEASE_MODEL_PATH = Path(os.getenv("DISEASE_MODEL_PATH", PROJECT_DIR / "models" / "plant_disease_resnet18.pth"))
    CROP_MODEL_PATH = Path(os.getenv("CROP_MODEL_PATH", PROJECT_DIR / "models" / "crop_random_forest.joblib"))
    WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
