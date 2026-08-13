import os

from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from app.database import create_table, save_question, get_questions


load_dotenv()

app = FastAPI()

create_table()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")



@app.post("/ask")
def ask(question: str):
    if not question.strip():
        raise HTTPException(
            status_code=400, 
            detail="質問が空です。質問を入力してください。"
        )
    
    try:
        response = client.responses.create(
            model="gpt-5.5",
            instructions="""
            あなたは技術文書を支援するAIアシスタントです。

            以下のルールに従って回答してください。

            - 技術的な内容を正確かつ分かりやすく説明する
            - 必要に応じて具体例を示す
            - 専門用語を使用する場合は簡単に説明する
            - 不明な情報については推測で断定しない
            - 回答は簡潔にまとめる
            """,
            input=question,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID],
                }
            ],
            max_output_tokens=1000
        )
        
        save_question(question, response.output_text)

        return {
            "question": question,
            "answer": response.output_text,
            "model": response.model,
            "token_usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens

            }
        }

    except Exception as e:
        print("ERROR:" , repr(e))
        raise HTTPException(
            status_code=500, 
            detail=str(e)
            )
    

@app.get("/history")
def history():
    rows = get_questions()

    return [
        {
            "id": row[0],
            "question": row[1],
            "answer": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]
