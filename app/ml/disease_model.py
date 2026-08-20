import cv2
import numpy as np

try:
    import torch
    import torch.nn as nn
    from torchvision import models, transforms

    TORCH_AVAILABLE = True
except (ImportError, ModuleNotFoundError, OSError):
    torch = None
    nn = None
    models = None
    transforms = None
    TORCH_AVAILABLE = False

from ..services.treatments import treatment_for


DEFAULT_CLASS_NAMES = [
    "Apple Scab",
    "Corn Common Rust",
    "Grape Black Rot",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Healthy",
]


class DiseaseClassifier:
    def __init__(self, model_path, device=None):
        self.model_path = model_path
        self.class_names = DEFAULT_CLASS_NAMES
        self.device = "cpu"
        self.model = None
        self.model_version = "heuristic-fallback"
        self.transform = None

        if TORCH_AVAILABLE and self.model_path.exists():
            self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self._build_model()
            self.transform = transforms.Compose(
                [
                    transforms.ToPILImage(),
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                ]
            )
            self._load_weights()

    def _build_model(self):
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, len(self.class_names))
        model.to(self.device)
        model.eval()
        return model

    def _load_weights(self):
        if not TORCH_AVAILABLE or self.model is None or not self.model_path.exists():
            return
        checkpoint = torch.load(self.model_path, map_location=self.device)
        state_dict = checkpoint.get("model_state_dict", checkpoint)
        if isinstance(checkpoint, dict) and "class_names" in checkpoint:
            self.class_names = checkpoint["class_names"]
            self.model.fc = nn.Linear(self.model.fc.in_features, len(self.class_names)).to(self.device)
        self.model.load_state_dict(state_dict)
        self.model_version = checkpoint.get("model_version", "resnet18-custom") if isinstance(checkpoint, dict) else "resnet18-custom"

    def predict(self, image_path):
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Uploaded file is not a readable image.")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.model_version != "heuristic-fallback" and self.model is not None and self.transform is not None:
            tensor = self.transform(rgb).unsqueeze(0).to(self.device)
            with torch.no_grad():
                logits = self.model(tensor)
                probabilities = torch.softmax(logits, dim=1)[0]
                confidence, index = torch.max(probabilities, dim=0)
            label = self.class_names[index.item()]
            return {
                "disease_name": label,
                "confidence": float(confidence.item()),
                "treatment": treatment_for(label),
                "model_version": self.model_version,
            }

        return self._heuristic_predict(rgb)

    def _heuristic_predict(self, rgb):
        resized = cv2.resize(rgb, (224, 224))
        hsv = cv2.cvtColor(resized, cv2.COLOR_RGB2HSV)

        green_mask = cv2.inRange(hsv, np.array([35, 35, 35]), np.array([90, 255, 255]))
        yellow_mask = cv2.inRange(hsv, np.array([18, 45, 45]), np.array([34, 255, 255]))
        brown_mask = cv2.inRange(hsv, np.array([5, 45, 20]), np.array([22, 255, 180]))
        dark_mask = cv2.inRange(hsv, np.array([0, 20, 0]), np.array([180, 255, 70]))

        total = resized.shape[0] * resized.shape[1]
        green = np.count_nonzero(green_mask) / total
        yellow = np.count_nonzero(yellow_mask) / total
        brown = np.count_nonzero(brown_mask) / total
        dark = np.count_nonzero(dark_mask) / total

        if green < 0.08:
            label = "Unknown Leaf Stress"
            confidence = 0.58
        elif brown + dark > 0.22:
            label = "Tomato Early Blight"
            confidence = min(0.93, 0.65 + brown + dark)
        elif yellow > 0.25:
            label = "Tomato Late Blight"
            confidence = min(0.9, 0.62 + yellow)
        elif brown > 0.12:
            label = "Apple Scab"
            confidence = min(0.88, 0.64 + brown)
        else:
            label = "Healthy"
            confidence = min(0.97, 0.72 + green / 3)

        return {
            "disease_name": label,
            "confidence": float(confidence),
            "treatment": treatment_for(label),
            "model_version": self.model_version,
            "metrics": {
                "green_ratio": round(float(green), 4),
                "yellow_ratio": round(float(yellow), 4),
                "brown_ratio": round(float(brown), 4),
                "dark_ratio": round(float(dark), 4),
            },
        }
