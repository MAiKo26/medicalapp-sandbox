from fastapi import  HTTPException, Response
import datetime
import bcrypt
from src.db.models import UserRegister,UserLogin
from src.db.database import users_collection
from dotenv import load_dotenv
import os
from jose import jwt


load_dotenv()


def register_user_service(UserRegister: UserRegister):
    resp = users_collection.find_one({"email": UserRegister.email})
    if resp:
        raise HTTPException(status_code=400, detail="Email Already Exists!")

    hashed_password = bcrypt.hashpw(UserRegister.password.encode("utf-8"), bcrypt.gensalt())

    user_document = {
            "fullname": UserRegister.fullname,
            "email": UserRegister.email,
            "password": hashed_password.decode("utf-8"),
            "role": UserRegister.role or "patient",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
        }

    users_collection.insert_one(user_document)

    return {"status_code": 200, "detail": "User Created Successfully!"}

def login_user_service(UserLogin:UserLogin):
    resp = users_collection.find_one({"email": UserLogin.email})
    if resp:
        if not bcrypt.checkpw(
            UserLogin.password.encode("utf-8"), resp["password"].encode("utf-8")
            ):
            raise HTTPException(status_code=400, detail="Invalid Password")
        else:
            token = jwt.encode(
                {
                "email": UserLogin.email, 
                "role": resp["role"],
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
                },
                os.getenv("SECRET_KEY"),
                algorithm=os.getenv("ENCODING_ALGORITHM"),
            )
            response = Response(content="Login successful") 
            response.set_cookie(
                    key="token", 
                    value=token, 
                    httponly=True,  
                    secure=False,   
                    samesite="lax"  
                )
            return response
    else:
        raise HTTPException(status_code=400, detail="User not found")

def identify_token_service(token:str):
    jwt_decoded = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ENCODING_ALGORITHM")]
    )
    user = users_collection.find_one({"email": jwt_decoded["email"]})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])

    return user
