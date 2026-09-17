"""
Generates a synthetic-but-realistic student placement dataset.

Replace `generate_dataset()` with a loader for your institution's real
historical placement records when you have them — just keep the same
column names, since the router and React form are both built around
this exact schema:

cgpa, tenth_percentage, twelfth_percentage, backlogs, internships,
projects, certifications, aptitude_score, technical_score,
communication_score, coding_score, branch
    -> placed (0/1), package_lpa (float)
"""
import numpy as np
import pandas as pd

from app.ml.skills_taxonomy import CAREERS

BRANCHES = ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "AI/ML"]


def _pick_career(row: pd.Series, rng: np.random.Generator) -> str:
    """Deterministic-ish heuristic so career labels correlate with skill
    scores, giving the classifier real signal to learn from. All options
    are kept on a comparable ~0-100 scale so no single career dominates
    by construction."""
    cgpa_100 = row.cgpa * 10  # rescale 0-10 -> 0-100 for comparability

    scores = {
        "Software Development Engineer": row.coding_score * 0.55 + row.technical_score * 0.35 + row.projects * 2,
        "Data Scientist / ML Engineer": row.technical_score * 0.45 + cgpa_100 * 0.35 + row.aptitude_score * 0.2,
        "Frontend Developer": row.coding_score * 0.4 + row.communication_score * 0.4 + row.projects * 3,
        "Backend Developer": row.coding_score * 0.5 + row.technical_score * 0.35 + row.projects * 2,
        "DevOps / Cloud Engineer": row.technical_score * 0.4 + row.certifications * 8 + row.coding_score * 0.25,
        "QA / Test Engineer": row.communication_score * 0.45 + row.aptitude_score * 0.45,
        "Business Analyst": row.communication_score * 0.55 + row.aptitude_score * 0.35,
        "Core / Hardware Engineer": (100 - row.coding_score) * 0.35 + cgpa_100 * 0.4,
    }
    if row.branch in ("Mechanical", "Civil", "EEE"):
        scores["Core / Hardware Engineer"] += 20
    if row.branch == "AI/ML":
        scores["Data Scientist / ML Engineer"] += 15
    for k in scores:
        scores[k] += rng.normal(0, 9)
    return max(scores, key=scores.get)


def generate_dataset(n: int = 4000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "cgpa": np.clip(rng.normal(7.2, 1.0, n), 4.5, 10.0).round(2),
        "tenth_percentage": np.clip(rng.normal(78, 10, n), 40, 100).round(1),
        "twelfth_percentage": np.clip(rng.normal(75, 10, n), 40, 100).round(1),
        "backlogs": rng.poisson(0.6, n).clip(0, 8),
        "internships": rng.poisson(0.8, n).clip(0, 5),
        "projects": rng.poisson(1.5, n).clip(0, 8),
        "certifications": rng.poisson(1.2, n).clip(0, 6),
        "aptitude_score": np.clip(rng.normal(65, 15, n), 10, 100).round(1),
        "technical_score": np.clip(rng.normal(63, 16, n), 10, 100).round(1),
        "communication_score": np.clip(rng.normal(68, 14, n), 10, 100).round(1),
        "coding_score": np.clip(rng.normal(60, 18, n), 5, 100).round(1),
        "branch": rng.choice(BRANCHES, n),
    })

    propensity = (
        df.cgpa * 6.5
        + df.aptitude_score * 0.35
        + df.technical_score * 0.35
        + df.communication_score * 0.20
        + df.coding_score * 0.30
        + df.internships * 4.0
        + df.projects * 2.0
        + df.certifications * 1.5
        - df.backlogs * 8.0
        + rng.normal(0, 12, n)
    )
    threshold = np.percentile(propensity, 42)  # ~58% placement rate
    df["placed"] = (propensity > threshold).astype(int)

    base_package = (
        2.5
        + (df.cgpa - 6) * 0.9
        + df.technical_score * 0.03
        + df.coding_score * 0.035
        + df.internships * 0.4
        + df.certifications * 0.15
        + rng.normal(0, 0.8, n)
    )
    df["package_lpa"] = np.where(df.placed == 1, np.clip(base_package, 2.0, 45.0).round(2), 0.0)

    df["career"] = df.apply(lambda row: _pick_career(row, rng), axis=1)

    return df


if __name__ == "__main__":
    data = generate_dataset()
    print(data.head())
    print(data.shape)
    print(data.placed.value_counts(normalize=True))
