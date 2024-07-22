from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    archive = Column(Boolean, default=False)

    # Relationships
    questions = relationship("Question", back_populates="user")
    answers = relationship("Answer", back_populates="user")
