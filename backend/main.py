from fastapi import FastAPI
from fastapi import APIRouter
from src.routes import chat,auth,users,ai
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

v1_router = APIRouter(prefix="/api/v1")



v1_router.include_router(chat.router)
v1_router.include_router(users.router)
v1_router.include_router(auth.router)
v1_router.include_router(ai.router)

app.include_router(v1_router);