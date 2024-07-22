from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from backend.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    archive = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
