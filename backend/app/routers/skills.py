"""
Module 7 — Skill Gap Analysis. Compares known skills (from the latest
resume upload, and/or manually supplied) against the requirement
profile for a target career, both defined in skills_taxonomy.py.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user
from app.database import resumes_collection
from app.ml.skills_taxonomy import CAREER_REQUIREMENTS
from app.ml.skill_gap import compute_skill_gap, generate_roadmap
from app import schemas

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("/careers")
async def list_careers():
    """Career tracks the skill-gap tool supports."""
    return {"careers": list(CAREER_REQUIREMENTS.keys())}


async def _resolve_known_skills(payload: schemas.SkillGapRequest, user_id: str) -> list:
    skills = set(payload.known_skills)
    if payload.use_latest_resume:
        resume = await resumes_collection.find_one(
            {"user_id": user_id}, sort=[("uploaded_at", -1)]
        )
        if resume and resume.get("extracted_skills"):
            skills.update(resume["extracted_skills"])
    return list(skills)


@router.post("/gap-analysis", response_model=schemas.SkillGapOut)
async def gap_analysis(
    payload: schemas.SkillGapRequest,
    current_user: dict = Depends(get_current_user),
):
    known_skills = await _resolve_known_skills(payload, current_user["id"])
    try:
        result = compute_skill_gap(known_skills, payload.target_career)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return schemas.SkillGapOut(**result, available_careers=list(CAREER_REQUIREMENTS.keys()))


@router.post("/roadmap", response_model=schemas.RoadmapOut)
async def learning_roadmap(
    payload: schemas.SkillGapRequest,
    current_user: dict = Depends(get_current_user),
):
    """Module 8 — turns Module 7's missing skills into an ordered set of
    learning stages for the same target career."""
    known_skills = await _resolve_known_skills(payload, current_user["id"])
    try:
        gap = compute_skill_gap(known_skills, payload.target_career)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    stages = generate_roadmap(payload.target_career, gap["missing_skills"])
    return schemas.RoadmapOut(target_career=payload.target_career, stages=stages)
