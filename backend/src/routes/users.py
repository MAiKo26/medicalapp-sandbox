from fastapi import APIRouter, HTTPException
from src.db.database import users_collection
from src.db.models import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])



@router.get("/")
async def all_users():
    try:
        users = list(users_collection.find({}, {"_id": 0}))
        return users
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.put("/{user_email}")
async def update_user(user_email: str, user: UserUpdate):
    try:
        updated_user = dict(user)
        result = users_collection.update_one(
            {"email": user_email}, {"$set": updated_user}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User updated successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Could not update user")


@router.delete("/{user_email}")
async def delete_user(user_email: str):
    try:
        result = users_collection.delete_one({"email": user_email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Could not delete user")
