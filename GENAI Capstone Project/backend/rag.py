import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from groq import Groq

from backend.vector_store import (
    create_embeddings,
    store_embeddings,
    search_similar_chunks
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

print("RAG LOADED...")


def load_pdf(file_path):

    loader = PyPDFLoader(file_path)

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(docs)

    text_chunks = []

    for chunk in chunks:

        text_chunks.append(
            chunk.page_content
        )

    embeddings = create_embeddings(
        text_chunks
    )

    store_embeddings(
        text_chunks,
        embeddings,
        os.path.basename(file_path)
    )

    return len(text_chunks)


def ask_question(question):

    result = search_similar_chunks(
        question
    )

    retrieved_chunks = result["chunks"]

    source = result["source"]

    score = result["score"]

    context = "\n".join(
        retrieved_chunks
    )

    prompt = f"""
    You are a helpful AI assistant.

    Answer the user's question ONLY using the provided context.

    If the answer is not available in the context, say:
    "I could not find the answer in the uploaded document."

    Context:
    {context}

    User Question:
    {question}

    Answer:
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "source": source,
        "score": score
    }