from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

from app.models import User
from app.schemas import UserResponse
from typing import List

app = FastAPI(title="CodeVerity API")

@app.get("/")
def read_root():
    return {"message": "CodeVerity API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT COUNT(*) FROM users"))
    count = result.scalar()
    return {"database": "connected", "user_count": count}

@app.get("/users-test", response_model=List[UserResponse])
def users_test(db: Session = Depends(get_db)):
    return db.query(User).all()