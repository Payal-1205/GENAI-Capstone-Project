import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Embedding dimension
dimension = 384

# FAISS Index
index = faiss.IndexFlatL2(dimension)

# Store chunks
document_chunks = []

# Store metadata
metadata = []


def create_embeddings(text_chunks):

    embeddings = embedding_model.encode(
        text_chunks,
        show_progress_bar=True
    )

    return np.array(embeddings).astype("float32")


def store_embeddings(
    text_chunks,
    embeddings,
    source_file
):

    index.add(embeddings)

    document_chunks.extend(text_chunks)

    for chunk in text_chunks:

        metadata.append(
            {
                "source": source_file,
                "chunk": chunk
            }
        )

    print(f"Added {len(text_chunks)} chunks to FAISS.")
    print(f"Total Chunks: {len(document_chunks)}")


def search_similar_chunks(question, k=3):

    if len(document_chunks) == 0:

        return {
            "chunks": ["No documents uploaded yet."],
            "source": "None",
            "score": 0
        }

    question_embedding = embedding_model.encode(
        [question]
    )

    distances, indices = index.search(
        np.array(question_embedding).astype("float32"),
        k=k
    )

    retrieved_chunks = []

    best_source = "Unknown"

    best_score = 0

    for rank, idx in enumerate(indices[0]):

        if idx != -1:

            retrieved_chunks.append(
                document_chunks[idx]
            )

            if rank == 0:

                best_source = metadata[idx]["source"]

                best_score = float(
                    distances[0][0]
                )

    return {
        "chunks": retrieved_chunks,
        "source": best_source,
        "score": best_score
    }