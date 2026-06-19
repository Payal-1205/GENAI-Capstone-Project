# GENAI-Capstone-Project
Healthcare Mediassist AI Copilot

Project Overview

Healthcare MediAssist AI is a Retrieval-Augmented Generation (RAG) based chatbot that enables users to upload healthcare documents and ask questions using natural language. The system retrieves relevant document chunks through semantic search and generates context-aware responses using a Large Language Model (LLM).

Milestone-1

The first milestone focuses on building the core RAG pipeline:

PDF Document Upload
Unified Document Parsing
Text Chunking
Embedding Generation
FAISS Vector Database
Semantic Similarity Search
Top-K Chunk Retrieval
Similarity Score Display
FastAPI Backend
Streamlit Frontend

Project Structure
Healthcare_Mediassist_AI/
│
├── frontend/
│   └── streamlit_app.py
│
├── backend/
│   ├── app.py
│   ├── rag.py
│   └── vector_store.py
│
├── uploads/
│
├── project_documents/
│   ├── requirements/
│   ├── architecture/
│   ├── tracker/
│   └── technical_document/
│
├── requirements.txt
├── .env
|--README.md

Running the Application
Start Backend
uvicorn backend.app:app --reload

Start Frontend
streamlit run frontend/app.py
