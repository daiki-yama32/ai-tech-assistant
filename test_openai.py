import os 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-5.5",    
    input="固有受容感覚とは何ですか？",
    max_output_tokens=1000
)

print("回答：")
print(response.output_text)
print("")

print("--- Token Usage ---")
print(f"Input Tokens: {response.usage.input_tokens}")
print(f"Output Tokens: {response.usage.output_tokens}")
print(f"Total Tokens: {response.usage.total_tokens}")
print("")

print("--- Full Response ---")
print(response)
