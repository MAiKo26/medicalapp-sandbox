from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from typing import Optional


class User(BaseModel):
    _id: str
    fullname: str
    email: EmailStr
    password: str
    role: str = Field(pattern="^(patient|doctor)$")
    created_at: str = datetime.now()
    updated_at: str = datetime.now()



class UserRegister(BaseModel):
    email: str
    fullname: str
    password: str
    role: Optional[str] = "patient"



class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    fullname: str
    password: str
    role: str
    