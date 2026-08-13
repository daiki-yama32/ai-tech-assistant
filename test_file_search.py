from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

vector_store_id = "vs_6a7d24d9b7a48191bd26006fca90f510"

response = client.responses.create(
    model="gpt-4.1-mini",
    input="この技術文書に書かれているモーターの最大回転数はいくつですか？",
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [vector_store_id],
        }
    ],
)

print(response.output_text)