from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers import auth, courses, submissions

app = FastAPI(title="CodeVerity API")
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(submissions.router)

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