TREATMENTS = {
    "Apple Scab": [
        "Remove infected leaves and fruit from the field.",
        "Apply a recommended fungicide during humid weather.",
        "Improve pruning to increase airflow.",
    ],
    "Tomato Early Blight": [
        "Remove lower infected leaves.",
        "Use copper or chlorothalonil fungicide as locally recommended.",
        "Avoid overhead irrigation.",
    ],
    "Tomato Late Blight": [
        "Destroy infected plant material immediately.",
        "Apply protective fungicide and avoid leaf wetness.",
        "Use resistant varieties next season.",
    ],
    "Corn Common Rust": [
        "Use resistant hybrids when possible.",
        "Apply fungicide if disease appears before tasseling.",
        "Remove crop residue after harvest.",
    ],
    "Grape Black Rot": [
        "Prune infected canes and mummified fruit.",
        "Apply fungicide before rainfall events.",
        "Improve canopy airflow.",
    ],
    "Healthy": [
        "No disease detected from the image.",
        "Continue regular monitoring.",
        "Maintain balanced watering and fertilizer schedule.",
    ],
    "Unknown Leaf Stress": [
        "Upload a clearer close-up leaf image for better diagnosis.",
        "Inspect the underside of the leaf for pests.",
        "Check soil moisture, drainage, and nutrient balance.",
    ],
}


def treatment_for(label):
    return TREATMENTS.get(label, TREATMENTS["Unknown Leaf Stress"])
