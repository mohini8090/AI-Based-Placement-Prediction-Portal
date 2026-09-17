"""
Module 6 — Career Recommendation. Reuses the same student input shape
as Module 5 (Placement Prediction), but through its own model and its
own collection — the two are related but conceptually separate results.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user
from app.database import career_recommendations_collection
from app.ml.career_predictor import recommender
from app import schemas
from app.utils import serialize_doc

router = APIRouter(prefix="/api/career", tags=["career"])


@router.post("/recommend", response_model=schemas.CareerRecommendationOut)
async def recommend_career(
    payload: schemas.StudentInput,
    current_user: dict = Depends(get_current_user),
):
    try:
        result = recommender.recommend(payload.model_dump())
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    doc = {
        "user_id": current_user["id"],
        "recommended_career": result["recommended_career"],
        "confidence": result["confidence"],
        "alternatives": result["alternatives"],
        "created_at": datetime.now(timezone.utc),
    }
    insert_result = await career_recommendations_collection.insert_one(doc)
    doc["_id"] = insert_result.inserted_id

    serialized = serialize_doc(doc)
    return schemas.CareerRecommendationOut(
        id=serialized["id"],
        recommended_career=serialized["recommended_career"],
        confidence=serialized["confidence"],
        alternatives=serialized["alternatives"],
        created_at=serialized["created_at"],
    )


@router.get("/latest", response_model=schemas.CareerRecommendationOut)
async def get_latest_recommendation(current_user: dict = Depends(get_current_user)):
    doc = await career_recommendations_collection.find_one(
        {"user_id": current_user["id"]}, sort=[("created_at", -1)]
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No career recommendation yet.")
    serialized = serialize_doc(doc)
    return schemas.CareerRecommendationOut(
        id=serialized["id"],
        recommended_career=serialized["recommended_career"],
        confidence=serialized["confidence"],
        alternatives=serialized["alternatives"],
        created_at=serialized["created_at"],
    )
