from flask import Blueprint, jsonify, request

from ..services.weather_service import fetch_weather


weather_bp = Blueprint("weather", __name__)


@weather_bp.get("/weather")
def weather():
    latitude = request.args.get("lat", "21.2514")
    longitude = request.args.get("lon", "81.6296")
    try:
        return jsonify(fetch_weather(latitude, longitude))
    except Exception:
        return jsonify(
            {
                "temperature": 34,
                "humidity": 68,
                "rainfall": 0,
                "wind_speed": 12,
                "source": "fallback",
            }
        )
