"""
Module 3 — Resume Upload & Parsing
Module 4 — Resume Analysis

Both live in one router since analysis happens immediately on upload —
there's no meaningful "parse now, analyze later" split at this scale.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.deps import get_current_user
from app.database import resumes_collection
from app.ml.resume_parser import extract_text, analyze_resume
from app import schemas
from app.utils import serialize_doc

router = APIRouter(prefix="/api/resumes", tags=["resumes"])

ALLOWED_EXTENSIONS = (".pdf", ".docx", ".txt")
MAX_FILE_SIZE_MB = 5


@router.post("/upload", response_model=schemas.ResumeAnalysisOut)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Upload a PDF, DOCX, or TXT resume.")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File is too large (max {MAX_FILE_SIZE_MB} MB).")

    try:
        text = extract_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text or len(text.strip()) < 30:
        raise HTTPException(status_code=422, detail="Couldn't read enough text from this file. Try a different export.")

    analysis = analyze_resume(text)

    doc = {
        "user_id": current_user["id"],
        "filename": file.filename,
        "raw_text": text,
        "extracted_skills": analysis["skills"],
        "extracted_email": analysis["email"],
        "extracted_phone": analysis["phone"],
        "word_count": analysis["word_count"],
        "ats_score": analysis["ats_score"],
        "sections_found": analysis["sections_found"],
        "suggestions": analysis["suggestions"],
        "uploaded_at": datetime.now(timezone.utc),
    }
    result = await resumes_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    return _to_out(doc)


@router.get("/latest", response_model=schemas.ResumeAnalysisOut)
async def get_latest_resume(current_user: dict = Depends(get_current_user)):
    doc = await resumes_collection.find_one(
        {"user_id": current_user["id"]}, sort=[("uploaded_at", -1)]
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No resume uploaded yet.")
    return _to_out(doc)


def _to_out(doc: dict) -> schemas.ResumeAnalysisOut:
    serialized = serialize_doc(doc)
    return schemas.ResumeAnalysisOut(
        id=serialized["id"],
        filename=serialized["filename"],
        ats_score=serialized["ats_score"],
        word_count=serialized["word_count"],
        email=serialized["extracted_email"],
        phone=serialized["extracted_phone"],
        sections_found=serialized["sections_found"],
        skills=serialized["extracted_skills"],
        suggestions=serialized["suggestions"],
        uploaded_at=serialized["uploaded_at"],
    )
