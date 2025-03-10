from fastapi import APIRouter, HTTPException
from jose import jwt
from src.db.models import UserRegister,UserLogin
from src.db.database import users_collection
from datetime import datetime
import bcrypt

from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register")
async def register_user(UserRegister: UserRegister):
    print("heyo")
    try:
        resp = users_collection.find_one({"email": UserRegister.email})
        print(UserRegister);
        if resp:
            raise HTTPException(status_code=400, detail="Email Already Exists!")

        hashed_password = bcrypt.hashpw(UserRegister.password.encode("utf-8"), bcrypt.gensalt())

        user_document = {
            "fullname": UserRegister.fullname,
            "email": UserRegister.email,
            "password": hashed_password.decode("utf-8"),
            # I put it patient by default then later we can change it by admin to a doctor if needed since we don't pass the role in the signup
            "role": UserRegister.role or "patient",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        users_collection.insert_one(user_document)

        return {"status_code": 200, "detail": "User Created Successfully!"}

    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.post("/login")
async def login_user(UserLogin:UserLogin):
    try:
        resp = users_collection.find_one({"email": UserLogin.email})
        if resp:
            if not bcrypt.checkpw(
                UserLogin.password.encode("utf-8"), resp["password"].encode("utf-8")
            ):
                raise HTTPException(status_code=400, detail="Invalid Password")
            else:
                token = jwt.encode(
                    {"email": UserLogin.email, "role": resp["role"]},
                    os.getenv("SECRET_KEY"),
                    algorithm=os.getenv("ENCODING_ALGORITHM"),
                )
                return {"token": token}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.get("/me")
async def identify_token(token: str):
    try:
        jwt_decoded = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ENCODING_ALGORITHM")]
        )
        user = users_collection.find_one({"email": jwt_decoded["email"]})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user["_id"] = str(user["_id"])

        return user
        
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Token")
