from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionCreate(BaseModel):
    question: str
    user_id: int