TARGET_NPK = {
    "rice": {"nitrogen": 80, "phosphorus": 40, "potassium": 40},
    "maize": {"nitrogen": 90, "phosphorus": 45, "potassium": 45},
    "cotton": {"nitrogen": 70, "phosphorus": 35, "potassium": 60},
    "mango": {"nitrogen": 55, "phosphorus": 35, "potassium": 70},
    "tomato": {"nitrogen": 80, "phosphorus": 50, "potassium": 80},
    "wheat": {"nitrogen": 100, "phosphorus": 50, "potassium": 40},
}


def suggest_fertilizer(payload):
    crop = payload.get("crop", "").strip().lower()
    target = TARGET_NPK.get(crop, {"nitrogen": 70, "phosphorus": 40, "potassium": 45})
    current = {
        "nitrogen": float(payload["nitrogen"]),
        "phosphorus": float(payload["phosphorus"]),
        "potassium": float(payload["potassium"]),
    }

    gaps = {key: target[key] - current[key] for key in target}
    limiting = max(gaps, key=gaps.get)

    if gaps[limiting] <= 0:
        return {
            "status": "Soil nutrients look balanced for this crop.",
            "recommendation": "Use compost or farmyard manure for maintenance only.",
            "details": gaps,
        }

    recommendation_map = {
        "nitrogen": "Apply urea or well-decomposed compost to improve nitrogen.",
        "phosphorus": "Apply DAP, SSP, or bone meal to improve phosphorus.",
        "potassium": "Apply muriate of potash, sulphate of potash, or wood ash carefully.",
    }

    return {
        "status": f"{limiting.title()} is the most limiting nutrient for {crop or 'selected crop'}.",
        "recommendation": recommendation_map[limiting],
        "details": gaps,
    }
