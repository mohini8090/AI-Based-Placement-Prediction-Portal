"""
Trains two scikit-learn models and saves them to app/ml/artifacts/:

1. placement_clf - RandomForestClassifier -> P(placed)
2. package_reg   - GradientBoostingRegressor -> expected package (LPA),
                    trained only on students who were placed

Run with (from backend/, venv active):
    python -m app.ml.train_model
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.ml.dataset import generate_dataset

ARTIFACT_DIR = Path(__file__).parent / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

NUMERIC_FEATURES = [
    "cgpa", "tenth_percentage", "twelfth_percentage", "backlogs",
    "internships", "projects", "certifications", "aptitude_score",
    "technical_score", "communication_score", "coding_score",
]
CATEGORICAL_FEATURES = ["branch"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def _preprocessor() -> ColumnTransformer:
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])


def train_placement_model(df: pd.DataFrame):
    X, y = df[FEATURES], df["placed"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipe = Pipeline([
        ("prep", _preprocessor()),
        ("clf", RandomForestClassifier(n_estimators=300, max_depth=10, min_samples_leaf=3, random_state=42, n_jobs=-1)),
    ])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    print(f"[placement_clf] accuracy={acc:.3f}  f1={f1:.3f}")
    print(classification_report(y_test, preds, target_names=["Not Placed", "Placed"]))
    return pipe, {"accuracy": acc, "f1": f1}


def train_package_model(df: pd.DataFrame):
    placed_df = df[df.placed == 1]
    X, y = placed_df[FEATURES], placed_df["package_lpa"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe = Pipeline([
        ("prep", _preprocessor()),
        ("reg", GradientBoostingRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=42)),
    ])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"[package_reg] MAE={mae:.3f} LPA")
    return pipe, {"mae_lpa": mae}


def train_career_model(df: pd.DataFrame):
    X, y = df[FEATURES], df["career"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipe = Pipeline([
        ("prep", _preprocessor()),
        ("clf", RandomForestClassifier(n_estimators=400, max_depth=12, min_samples_leaf=2, random_state=42, n_jobs=-1)),
    ])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"[career_clf] accuracy={acc:.3f}")
    print(classification_report(y_test, preds))
    return pipe, {"accuracy": acc, "classes": sorted(y.unique().tolist())}


def main():
    print("Generating training dataset...")
    df = generate_dataset(n=6000)

    print("\nTraining placement classifier...")
    placement_pipe, placement_metrics = train_placement_model(df)

    print("\nTraining package regressor...")
    package_pipe, package_metrics = train_package_model(df)

    print("\nTraining career recommender...")
    career_pipe, career_metrics = train_career_model(df)

    joblib.dump(placement_pipe, ARTIFACT_DIR / "placement_clf.joblib")
    joblib.dump(package_pipe, ARTIFACT_DIR / "package_reg.joblib")
    joblib.dump(career_pipe, ARTIFACT_DIR / "career_clf.joblib")

    metrics = {
        "placement_clf": placement_metrics,
        "package_reg": package_metrics,
        "career_clf": career_metrics,
    }
    with open(ARTIFACT_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved models + metrics to {ARTIFACT_DIR}")


if __name__ == "__main__":
    main()
