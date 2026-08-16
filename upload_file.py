from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import time
import os


load_dotenv()

client = OpenAI()

#====================
# Vector Storeを確認
#====================

# Vector Store IDを取得
vector_store_id = os.getenv("VECTOR_STORE_ID")

# Vector Storeが存在しない場合は新しく作成
if not vector_store_id:

    vector_store = client.vector_stores.create(
        name="technical_document_store",
    )

    vectore_store_id = vector_store.id

    print("新しいVector Storeを作成しました。")
    print("Vector Store ID:", vector_store_id)

    # .envにVector Store IDを保存
    with open(".env", "a", encoding="utf-8") as env_file:
        env_file.write(f"\nVECTOR_STORE_ID={vector_store_id}\n")

        print(".envにVector Store IDを保存しました。")

else:

    print("既存のVector Storeを使用します。")
    print("Vector Store ID:", vector_store_id)


#=======================
# documents内のPDFを取得
#=======================

documents_dir = Path("documents")

pdf_files = list(documents_dir.glob("*.pdf"))

print("■ 検出したPDF:")

for pdf_file in pdf_files:
    print(pdf_file.name)


#=======================
# Vector Storeに登録されているファイルを確認
#=======================

vector_store_files = client.vector_stores.files.list(
    vector_store_id=vector_store_id
)

registered_filenames = set()

for vector_store_file in vector_store_files.data:
    file_id = vector_store_file.id
    file_info = client.files.retrieve(file_id)
    registered_filenames.add(file_info.filename)

print("■ Vector Storeに登録されているファイル(重複除外):")

for filename in registered_filenames:
    print(filename)

# =========================
# PDFの重複チェック
# =========================

for pdf_file in pdf_files:
    filename = pdf_file.name
    if filename in registered_filenames:
        print(f" SKIP: {filename}")

    else:
        print(f" UPLOAD: {filename}")

        # PDFをOpenAI Filesへアップロード
        with open(pdf_file, "rb") as file:
            uploaded_file = client.files.create(
                file=file,
                purpose="assistants"
            )

        print("File ID: ", uploaded_file.id)

        #Vector Storeへ追加
        vector_store_file = client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=uploaded_file.id
        )

        print(
            "Vector Store File status: ",
            vector_store_file.status
        )

        # 登録完了まで待つ
        while True:

            vector_store_file = client.vector_stores.files.retrieve(
                vector_store_id=vector_store_id,
                file_id=uploaded_file.id
            )

            print(
                f"{filename}: {vector_store_file.status}"
            )

            if vector_store_file.status == "completed":
                print(f"登録完了： {filename}")
                break

            if vector_store_file.status in ["failed", "cancelled"]:
                raise RuntimeError(
                    f"{filename} の処理に失敗しました： "
                    f"{vector_store_file.status}"
                )

            time.sleep(2)
