from fastapi import APIRouter, HTTPException, Response,Cookie
from src.db.models import UserRegister,UserLogin
from src.services.auth_service import register_user_service, login_user_service,identify_token_service

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register")
async def register_user(UserRegister: UserRegister):
    try:
        return register_user_service(UserRegister)
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.post("/login")
async def login_user(UserLogin:UserLogin):
    try:
        return login_user_service(UserLogin)
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")

@router.post("/logout")
async def logout():
    response = Response(content="Logged out successfully")
    response.delete_cookie("token") 
    return response


@router.get("/me")
async def identify_token(token: str = Cookie(None)):
    if token is None:
        raise HTTPException(status_code=400, detail="No cookie found")
    try:
        return identify_token_service
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Token")
