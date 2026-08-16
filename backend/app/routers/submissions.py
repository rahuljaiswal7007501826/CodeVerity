from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import Submission, Assignment, User
from app.schemas import SubmissionCreate, SubmissionResponse
from app.auth import get_current_user, require_role

router = APIRouter(prefix="/submissions", tags=["Submissions"])

MAX_CODE_LENGTH = 50_000  # ~50KB, generous for a single assignment file
SUPPORTED_LANGUAGES = {"python", "java"}


@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("STUDENT"))
):
    # Validate assignment exists
    assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Validate language
    if submission.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language. Use one of: {SUPPORTED_LANGUAGES}")

    # Validate non-empty and size
    code_stripped = submission.code.strip()
    if not code_stripped:
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    if len(code_stripped) > MAX_CODE_LENGTH:
        raise HTTPException(status_code=400, detail="Code exceeds maximum allowed size")

    # Determine version (increment if resubmitting to same assignment)
    existing_count = db.query(func.count(Submission.id)).filter(
        Submission.student_id == current_user.id,
        Submission.assignment_id == submission.assignment_id
    ).scalar()

    new_submission = Submission(
        student_id=current_user.id,
        assignment_id=submission.assignment_id,
        code=code_stripped,
        language=submission.language.lower(),
        version=existing_count + 1
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission


@router.get("/my", response_model=List[SubmissionResponse])
def list_my_submissions(db: Session = Depends(get_db), current_user: User = Depends(require_role("STUDENT"))):
    return db.query(Submission).filter(Submission.student_id == current_user.id).all()


@router.get("/{submission_id}", response_model=SubmissionResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Students can only view their own; instructors can view any
    if current_user.role == "STUDENT" and submission.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view your own submissions")

    return submission


@router.get("/assignment/{assignment_id}", response_model=List[SubmissionResponse])
def list_submissions_for_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("INSTRUCTOR"))
):
    return db.query(Submission).filter(Submission.assignment_id == assignment_id).all()