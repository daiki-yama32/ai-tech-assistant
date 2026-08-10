from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

def generate_answer(question: str) -> str:
    # ここで質問に対する回答を生成するロジックを実装します
    return f"これは仮の回答です。あなたの質問は 「{question}」 です。"


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/ask")
def ask(request: QuestionRequest):
    answer = generate_answer(request.question)
    return {"answer": answer}
