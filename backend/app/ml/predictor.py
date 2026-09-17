"""
Loads the trained model artifacts once and exposes predict(), used by
the placement prediction router.
"""
from pathlib import Path
from typing import Dict

import joblib
import pandas as pd

from app.ml.train_model import FEATURES, ARTIFACT_DIR

_BENCHMARKS = {
    "cgpa": 8.0, "aptitude_score": 75, "technical_score": 75,
    "communication_score": 75, "coding_score": 75,
    "internships": 2, "projects": 3, "certifications": 2,
}
_FRIENDLY_NAMES = {
    "cgpa": "CGPA", "aptitude_score": "Aptitude score",
    "technical_score": "Technical knowledge", "communication_score": "Communication skills",
    "coding_score": "Coding proficiency", "internships": "Internship experience",
    "projects": "Project portfolio", "certifications": "Certifications",
}


class PlacementPredictor:
    def __init__(self, artifact_dir: Path = ARTIFACT_DIR):
        self.artifact_dir = artifact_dir
        self._placement_clf = None
        self._package_reg = None

    def _ensure_loaded(self):
        if self._placement_clf is None:
            missing = [
                name for name in ("placement_clf.joblib", "package_reg.joblib")
                if not (self.artifact_dir / name).exists()
            ]
            if missing:
                raise FileNotFoundError(
                    f"Model artifacts not found: {missing}. Run "
                    "`python -m app.ml.train_model` from the backend/ directory first."
                )
            self._placement_clf = joblib.load(self.artifact_dir / "placement_clf.joblib")
            self._package_reg = joblib.load(self.artifact_dir / "package_reg.joblib")

    def _skill_gaps(self, row: Dict):
        gaps = []
        for feature, benchmark in _BENCHMARKS.items():
            if row[feature] < benchmark:
                gaps.append(_FRIENDLY_NAMES[feature])
        return gaps[:5]

    def predict(self, student_input: Dict) -> Dict:
        self._ensure_loaded()
        X = pd.DataFrame([student_input])[FEATURES]

        proba = self._placement_clf.predict_proba(X)[0]
        placed_idx = list(self._placement_clf.classes_).index(1)
        placement_probability = float(proba[placed_idx])
        placement_status = "Likely Placed" if placement_probability >= 0.5 else "At Risk"

        predicted_package = None
        if placement_probability >= 0.35:
            predicted_package = round(float(self._package_reg.predict(X)[0]), 2)

        return {
            "placement_probability": round(placement_probability, 3),
            "placement_status": placement_status,
            "predicted_package_lpa": predicted_package,
            "top_skill_gaps": self._skill_gaps(student_input),
        }


predictor = PlacementPredictor()
