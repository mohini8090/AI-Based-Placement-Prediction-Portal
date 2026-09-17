"""
Compares a student's known skills against the requirement profile for a
target career track (Module 7), and turns the resulting gaps into an
ordered learning roadmap (Module 8).
"""
from app.ml.skills_taxonomy import CAREER_REQUIREMENTS, LEARNING_RESOURCES


def compute_skill_gap(known_skills: list, target_career: str) -> dict:
    if target_career not in CAREER_REQUIREMENTS:
        raise ValueError(f"Unknown career track: {target_career}")

    known_set = {s.strip() for s in known_skills}
    requirements = CAREER_REQUIREMENTS[target_career]

    matched, missing = [], []
    total_weight = sum(w for _, w in requirements)
    covered_weight = 0

    for skill, weight in requirements:
        if skill in known_set:
            matched.append({"skill": skill, "weight": weight})
            covered_weight += weight
        else:
            missing.append({"skill": skill, "weight": weight})

    # highest-weight gaps first — the ones that move the needle most
    missing.sort(key=lambda x: -x["weight"])

    readiness = round((covered_weight / total_weight) * 100, 1) if total_weight else 0

    return {
        "target_career": target_career,
        "readiness_percent": readiness,
        "matched_skills": matched,
        "missing_skills": missing,
    }


def generate_roadmap(target_career: str, missing_skills: list) -> list:
    """Turns the highest-priority skill gaps into an ordered set of
    learning stages, each with a handful of concrete topics."""
    roadmap = []
    for i, gap in enumerate(missing_skills[:5], start=1):
        skill = gap["skill"]
        topics = LEARNING_RESOURCES.get(
            skill, [f"Study the fundamentals of {skill}", "Build a small project using it"]
        )
        roadmap.append({
            "stage": i,
            "skill": skill,
            "priority": "High" if gap["weight"] >= 3 else "Medium" if gap["weight"] == 2 else "Low",
            "topics": topics,
        })
    return roadmap
