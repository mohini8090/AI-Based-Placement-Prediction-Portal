"""
Module 2 — Student Dashboard. Pulls together a snapshot from every other
module that exists so far.
"""
from fastapi import APIRouter, Depends

from app import schemas
from app.core.deps import get_current_user
from app.database import resumes_collection, predictions_collection, career_recommendations_collection

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

ALL_MODULES = [
    "User Registration & Login",
    "Student Dashboard",
    "Resume Upload & Parsing",
    "Resume Analysis",
    "Placement Prediction",
    "Career Recommendation",
    "Skill Gap Analysis",
    "Learning Roadmap",
    "Admin Dashboard",
]
UNLOCKED_SO_FAR = set(ALL_MODULES)  # all 9 modules are live


@router.get("/", response_model=schemas.DashboardOut)
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    latest_resume = await resumes_collection.find_one(
        {"user_id": current_user["id"]}, sort=[("uploaded_at", -1)]
    )
    latest_prediction = await predictions_collection.find_one(
        {"user_id": current_user["id"]}, sort=[("created_at", -1)]
    )
    latest_career_doc = await career_recommendations_collection.find_one(
        {"user_id": current_user["id"]}, sort=[("created_at", -1)]
    )
    total_predictions = await predictions_collection.count_documents(
        {"user_id": current_user["id"]}
    )

    prediction_out = None
    if latest_prediction:
        prediction_out = schemas.PredictionResult(
            id=str(latest_prediction["_id"]),
            placement_probability=latest_prediction["placement_probability"],
            placement_status=latest_prediction["placement_status"],
            predicted_package_lpa=latest_prediction.get("predicted_package_lpa"),
            top_skill_gaps=latest_prediction.get("top_skill_gaps", []),
            created_at=latest_prediction["created_at"],
        )

    return schemas.DashboardOut(
        full_name=current_user["full_name"],
        email=current_user["email"],
        role=current_user["role"],
        member_since=current_user["created_at"],
        modules_unlocked=[m for m in ALL_MODULES if m in UNLOCKED_SO_FAR],
        modules_upcoming=[m for m in ALL_MODULES if m not in UNLOCKED_SO_FAR],
        has_resume=latest_resume is not None,
        latest_resume_score=latest_resume["ats_score"] if latest_resume else None,
        total_predictions=total_predictions,
        latest_prediction=prediction_out,
        latest_career=latest_career_doc["recommended_career"] if latest_career_doc else None,
    )
