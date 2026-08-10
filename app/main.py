from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

def generate_answer(question: str) -> str:
    # ここで質問に対する回答を生成するロジックを実装します
    if "NVH" in question:
        return "NVHはNoise, Vibration, Harshnessの略語です。"
    if "ギヤ" in question or "ギア" in question:
        return "ギアノイズには、歯形誤差、噛み合い誤差、剛性変動などが影響します。"
    return f"申し訳ありません。その質問についてはまだ回答できません。あなたの質問は 「{question}」 です。"



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/ask")
def ask(request: QuestionRequest):
    answer = generate_answer(request.question)
    return {"answer": answer}
