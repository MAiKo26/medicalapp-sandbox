from fastapi import APIRouter, HTTPException
from src.db.models import UserUpdate
from src.services.users_service import get_all_users_service,update_user_service, delete_user_service


router = APIRouter(prefix="/users", tags=["users"])



@router.get("/")
async def all_users():
    try:
        return get_all_users_service()
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.put("/{user_email}")
async def update_user(user_email: str, user: UserUpdate):
    try:
        return update_user_service(user_email,user)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not update user")


@router.delete("/{user_email}")
async def delete_user(user_email: str):
    try:
        return delete_user_service(user_email)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not delete user")
