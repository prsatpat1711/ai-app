from fastapi import FastAPI, Depends
import google.generativeai as genai
import os
from backend.database import SessionLocal, engine, Base
from backend.profiles.models import User
from backend.answers.models import Answer
from backend.questions.models import Question
from backend.profiles.schemas import UserCreate, UserID
from backend.answers.schemas import AnswerCreate
from backend.questions.schemas import QuestionCreate
from sqlalchemy.orm import Session
import requests
from readability import Document
from bs4 import BeautifulSoup
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

app = FastAPI()

Base.metadata.create_all(engine)

genai.configure(api_key="AIzaSyCTofCTX4Vvfk28TTqUPYYCul6kZJDxD78")



model = genai.GenerativeModel('gemini-1.5-flash')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    response = model.generate_content("Write a story about Pratik the coder")
    user_query = db.query(User)
    all_users = user_query.all()
    return {"Response": response.text,
            "User": all_users}

@app.post("/create_user")
async def create_todo(user_body: UserCreate, db: Session = Depends(get_db)):
    user = User(name=user_body.name, email=user_body.email)
    db.add(user)
    db.commit()
    return {"User added": user.name}


@app.post("/generate_response")
async def generate_response(question_body: QuestionCreate, db: Session = Depends(get_db)):
    if question_body:
        question = Question(question=question_body.question, user_id=question_body.user_id)
        db.add(question)
        db.commit()
        google_custom_search_url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyDBX4d-8madXPyW5e7-v0T1Og3llkqBDAc&cx=54f24bf4066b04996&q={question.question}"
        google_response = requests.get(google_custom_search_url)
        google_response.raise_for_status()
        jsonified_google_response = google_response.json().get('items', [])
        sources = ""
        i = 0
        for item in jsonified_google_response:
            if i == 3:
                break
            web_response = requests.get(item.get('link', ''))
            doc = Document(web_response.text)
            summary_html = doc.summary()
            soup = BeautifulSoup(summary_html, 'lxml')
            web_result = soup.get_text()
            # Object of automatic summarization.
            auto_abstractor = AutoAbstractor()
            # Set tokenizer.
            auto_abstractor.tokenizable_doc = SimpleTokenizer()
            # Set delimiter for making a list of sentence.
            auto_abstractor.delimiter_list = [".", "\n"]
            # Object of abstracting and filtering document.
            abstractable_doc = TopNRankAbstractor()
            # Summarize document.
            result_dict = auto_abstractor.summarize(web_result, abstractable_doc)
            summarized_text = ' '.join(sentence for sentence in result_dict['summarize_result'])
            
            sources = sources + "\n\n" + summarized_text
            i = i + 1
        
        print(sources)
        response = model.generate_content(question.question + sources)
        answer = Answer(answer=response.text, user_id=question_body.user_id, question_id=question.id)
        db.add(answer)  
        db.commit()
        return {"Response": answer.answer}