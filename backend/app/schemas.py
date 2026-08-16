from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal
from typing import Optional, List

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

class CourseCreate(BaseModel):
    title: str

class CourseResponse(BaseModel):
    id: int
    title: str
    instructor_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AssignmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    language: str
    due_date: Optional[datetime] = None

class AssignmentResponse(BaseModel):
    id: int
    course_id: int
    title: str
    description: Optional[str]
    language: str
    due_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True