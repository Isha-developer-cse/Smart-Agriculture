import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def train(args):
    dataset_path = Path(args.dataset)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(dataset_path)
    missing = [column for column in FEATURES + ["label"] if column not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")

    x_train, x_test, y_train, y_test = train_test_split(
        df[FEATURES],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"],
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=250, random_state=42, class_weight="balanced")),
        ]
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(classification_report(y_test, predictions))
    joblib.dump(model, output_path)
    print(f"saved crop model to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train crop recommendation Random Forest model.")
    parser.add_argument("--dataset", default="data/crop_recommendation/Crop_recommendation.csv")
    parser.add_argument("--output", default="models/crop_random_forest.joblib")
    train(parser.parse_args())
