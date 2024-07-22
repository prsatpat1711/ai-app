from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnswerCreate(BaseModel):
    answer: str
    user_id: int
    question_id: int