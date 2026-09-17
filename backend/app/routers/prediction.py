"""
Module 5 — Placement Prediction.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user
from app.database import predictions_collection
from app.ml.predictor import predictor
from app import schemas
from app.utils import serialize_doc

router = APIRouter(prefix="/api/predict", tags=["prediction"])


@router.post("/", response_model=schemas.PredictionResult)
async def predict_placement(
    payload: schemas.StudentInput,
    current_user: dict = Depends(get_current_user),
):
    try:
        result = predictor.predict(payload.model_dump())
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    doc = {
        "user_id": current_user["id"],
        **payload.model_dump(),
        "placement_probability": result["placement_probability"],
        "placement_status": result["placement_status"],
        "predicted_package_lpa": result["predicted_package_lpa"],
        "top_skill_gaps": result["top_skill_gaps"],
        "created_at": datetime.now(timezone.utc),
    }
    insert_result = await predictions_collection.insert_one(doc)
    doc["_id"] = insert_result.inserted_id

    serialized = serialize_doc(doc)
    return schemas.PredictionResult(
        id=serialized["id"],
        placement_probability=serialized["placement_probability"],
        placement_status=serialized["placement_status"],
        # predicted_package_lpa=serialized["predicted_package_lpa"],
        top_skill_gaps=serialized["top_skill_gaps"],
        created_at=serialized["created_at"],
    )


@router.get("/history", response_model=list[schemas.PredictionHistoryOut])
async def get_history(current_user: dict = Depends(get_current_user)):
    cursor = predictions_collection.find(
        {"user_id": current_user["id"]}
    ).sort("created_at", -1)

    out = []
    async for doc in cursor:
        serialized = serialize_doc(doc)
        out.append(schemas.PredictionHistoryOut(
            id=serialized["id"],
            cgpa=serialized["cgpa"],
            branch=serialized["branch"],
            placement_probability=serialized["placement_probability"],
            placement_status=serialized["placement_status"],
            predicted_package_lpa=serialized["predicted_package_lpa"],
            top_skill_gaps=serialized["top_skill_gaps"],
            created_at=serialized["created_at"],
        ))
    return out
