from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Literal["STUDENT", "INSTRUCTOR", "ADMIN"]

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # allows reading directly from SQLAlchemy objects

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"