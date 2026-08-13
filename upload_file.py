from openai import OpenAI
from dotenv import load_dotenv
import time


load_dotenv()

client = OpenAI()

# PDFをアップロード
with open("technical_document.pdf", "rb") as file:
    uploaded_file = client.files.create(
        file=file,
        purpose="assistants"
    )

print("File ID:", uploaded_file.id)
print("File name:", uploaded_file.filename)


# Vector Storeを作成
vector_store = client.vector_stores.create(
    name="technical_document_store",
)

print ("Vector Store ID:", vector_store.id)


# PDFをVector Storeに追加
vector_store_file = client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=uploaded_file.id
)

print("Vector Store file status:", vector_store_file.status)


# 登録完了まで待つ
while True:
    vector_store_file = client.vector_stores.files.retrieve(
        vector_store_id=vector_store.id,
        file_id=uploaded_file.id
    )
    if vector_store_file.status == "completed":
        break
    if vector_store_file.status in ["failed", "cancelled"]:
        raise RuntimeError(
            f"File processing failed: {vector_store_file.status}"
            )

    time.sleep(2)

print("PDF is ready for File Search!")