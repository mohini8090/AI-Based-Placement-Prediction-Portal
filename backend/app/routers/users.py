"""
Basic user profile endpoint.
"""
from fastapi import APIRouter, Depends

from app import schemas
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return schemas.UserOut(**current_user)
