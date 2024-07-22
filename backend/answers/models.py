from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from backend.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    answer = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    archive = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
