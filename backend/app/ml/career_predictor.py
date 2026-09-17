"""
Loads the trained career classifier and returns a ranked shortlist —
used by Module 6 (Career Recommendation).
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from app.ml.train_model import FEATURES, ARTIFACT_DIR


class CareerRecommender:
    def __init__(self, artifact_dir: Path = ARTIFACT_DIR):
        self.artifact_dir = artifact_dir
        self._career_clf = None

    def _ensure_loaded(self):
        if self._career_clf is None:
            path = self.artifact_dir / "career_clf.joblib"
            if not path.exists():
                raise FileNotFoundError(
                    "career_clf.joblib not found. Run `python -m app.ml.train_model` "
                    "from the backend/ directory first."
                )
            self._career_clf = joblib.load(path)

    def recommend(self, student_input: dict, top_n: int = 3) -> dict:
        self._ensure_loaded()
        X = pd.DataFrame([student_input])[FEATURES]

        proba = self._career_clf.predict_proba(X)[0]
        classes = self._career_clf.classes_
        order = np.argsort(proba)[::-1][:top_n]

        alternatives = [
            {"career": classes[i], "confidence": round(float(proba[i]), 3)}
            for i in order
        ]
        return {
            "recommended_career": alternatives[0]["career"],
            "confidence": alternatives[0]["confidence"],
            "alternatives": alternatives,
        }


recommender = CareerRecommender()
