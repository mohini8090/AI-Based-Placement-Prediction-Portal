"""
Module 9 — Admin Dashboard. Read-only aggregation across all students —
placement rate, branch breakdown, and a per-student table. Gated by
require_admin, which checks the `role` field set on the user document.
"""
from collections import Counter

from fastapi import APIRouter, Depends

from app import schemas
from app.core.deps import require_admin
from app.database import (
    users_collection,
    resumes_collection,
    predictions_collection,
    career_recommendations_collection,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=schemas.AdminStatsOut)
async def get_stats(_: dict = Depends(require_admin)):
    total_students = await users_collection.count_documents({"role": "student"})
    total_predictions = await predictions_collection.count_documents({})

    placed_count = await predictions_collection.count_documents(
        {"placement_status": "Likely Placed"}
    )
    placement_rate = round((placed_count / total_predictions) * 100, 1) if total_predictions else 0.0

    branch_counts = Counter()
    package_values = []
    async for doc in predictions_collection.find({}, {"branch": 1, "predicted_package_lpa": 1}):
        if doc.get("branch"):
            branch_counts[doc["branch"]] += 1
        if doc.get("predicted_package_lpa"):
            package_values.append(doc["predicted_package_lpa"])

    avg_package = round(sum(package_values) / len(package_values), 2) if package_values else None

    career_counts = Counter()
    async for doc in career_recommendations_collection.find({}, {"recommended_career": 1}):
        if doc.get("recommended_career"):
            career_counts[doc["recommended_career"]] += 1

    return schemas.AdminStatsOut(
        total_students=total_students,
        total_predictions=total_predictions,
        placement_rate_percent=placement_rate,
        average_predicted_package=avg_package,
        branch_breakdown=dict(branch_counts.most_common()),
        top_recommended_careers=dict(career_counts.most_common(5)),
    )


@router.get("/students", response_model=list[schemas.AdminStudentOut])
async def list_students(_: dict = Depends(require_admin)):
    out = []
    async for user in users_collection.find({"role": "student"}):
        user_id = str(user["_id"])

        total_predictions = await predictions_collection.count_documents({"user_id": user_id})
        latest_prediction = await predictions_collection.find_one(
            {"user_id": user_id}, sort=[("created_at", -1)]
        )
        latest_resume = await resumes_collection.find_one(
            {"user_id": user_id}, sort=[("uploaded_at", -1)]
        )
        latest_career = await career_recommendations_collection.find_one(
            {"user_id": user_id}, sort=[("created_at", -1)]
        )

        out.append(schemas.AdminStudentOut(
            id=user_id,
            full_name=user["full_name"],
            email=user["email"],
            total_predictions=total_predictions,
            latest_placement_status=latest_prediction["placement_status"] if latest_prediction else None,
            latest_probability=latest_prediction["placement_probability"] if latest_prediction else None,
            has_resume=latest_resume is not None,
            latest_career=latest_career["recommended_career"] if latest_career else None,
        ))
    return out
