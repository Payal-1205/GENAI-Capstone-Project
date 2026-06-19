import os

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from fastapi.middleware.cors import CORSMiddleware

from backend.rag import (
    load_pdf,
    ask_question
)

from backend.vector_store import (
    search_similar_chunks
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

print("APP STARTING...")


@app.get("/")
def home():

    return {
        "message":
        "Welcome to the RAG API. Backend is running successfully."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    try:

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(
                await file.read()
            )

        chunks = load_pdf(
            file_path
        )

        return {
            "message":
            f"File '{file.filename}' uploaded and processed successfully.",
            "chunks_created": chunks
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/retrieve")
async def retrieve(data: dict):

    try:

        query = data["query"]

        result = search_similar_chunks(
            query
        )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }


@app.post("/chat")
async def chat(data: dict):

    try:

        question = data["question"]

        result = ask_question(
            question
        )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }