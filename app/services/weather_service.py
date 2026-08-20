import requests
from flask import current_app


def fetch_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
    }
    response = requests.get(current_app.config["WEATHER_BASE_URL"], params=params, timeout=8)
    response.raise_for_status()
    current = response.json()["current"]
    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "rainfall": current["precipitation"],
        "wind_speed": current["wind_speed_10m"],
    }
