import os

from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



@app.post("/ask")
def ask(question: str):
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
            max_output_tokens=1000
        )
        
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
        raise HTTPException(
            status_code=500, 
            detail=str("AIへの問い合わせ中にエラーが発生しました。")
            )
    

