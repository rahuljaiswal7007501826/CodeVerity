from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.database import Base
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))

    assignments = relationship("Assignment", back_populates="course", cascade="all, delete")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    language = Column(String(20), nullable=False)
    due_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))

    course = relationship("Course", back_populates="assignments")