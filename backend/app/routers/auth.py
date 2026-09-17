"""
Module 1 — Registration and login. Issues JWT bearer tokens.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.core.security import hash_password, verify_password, create_access_token
from app.database import users_collection
from app.utils import serialize_doc

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
async def register(payload: schemas.UserCreate):
    existing = await users_collection.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    doc = {
        "full_name": payload.full_name,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "role": "student",
        "created_at": datetime.now(timezone.utc),
    }
    result = await users_collection.insert_one(doc)
    doc["_id"] = result.inserted_id

    user = serialize_doc(doc)
    token = create_access_token({"sub": user["id"]})
    return schemas.Token(access_token=token, user=schemas.UserOut(**user))


@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm uses `username` for the identifier field; we treat it as email
    doc = await users_collection.find_one({"email": form_data.username})
    if not doc or not verify_password(form_data.password, doc["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    user = serialize_doc(doc)
    token = create_access_token({"sub": user["id"]})
    return schemas.Token(access_token=token, user=schemas.UserOut(**user))
