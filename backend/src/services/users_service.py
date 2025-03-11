from fastapi import HTTPException
from src.db.models import UserUpdate
from src.db.database import users_collection


def get_all_users_service():
    users = list(users_collection.find({}, {"_id": 0}))
    return users

def update_user_service(user_email: str, user: UserUpdate):
    updated_user = dict(user)
    result = users_collection.update_one(
        {"email": user_email}, {"$set": updated_user}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User updated successfully"}

def delete_user_service(user_email:str):
    result = users_collection.delete_one({"email": user_email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
