# 🏥 Hospital Policy Assistant

An Enterprise AI-powered **Hospital Policy Assistant** built using **LangChain**, **FastAPI**, **ChromaDB**, **Conversational RAG**, and **Ollama/OpenAI**.

The application enables healthcare professionals to ask natural language questions about hospital documents such as SOPs, HR policies, compliance manuals, infection control guidelines, and quality procedures.

---

# Features

* Conversational RAG (Retrieval-Augmented Generation)
* Session-based conversation memory
* Multi-document search
* Chroma Vector Database
* PDF, DOCX, TXT document support
* FastAPI REST APIs
* Modular Architecture
* Loguru Logging
* Source Document Citations
* Health Check APIs
* Collection Statistics
* Memory Management
* Enterprise Ready

---

# Technology Stack

| Technology             | Purpose                     |
| ---------------------- | --------------------------- |
| Python 3.11+           | Programming Language        |
| FastAPI                | REST API                    |
| LangChain              | LLM Framework               |
| ChromaDB               | Vector Database             |
| HuggingFace Embeddings | Embeddings                  |
| Ollama / OpenAI        | Large Language Model        |
| Loguru                 | Logging                     |
| Pydantic               | Request/Response Validation |
| Uvicorn                | ASGI Server                 |

---

# Project Architecture

```
Client
    │
    ▼
FastAPI Router
    │
    ▼
Service Layer
    │
    ▼
Implementation Layer
    │
    ├──────────────┐
    ▼              ▼
Vector Store   Conversation Memory
    │
    ▼
ChromaDB
    │
    ▼
LLM
```

---

# Project Structure

```
Hospital_Policy_Assistant/
│
├── implementations/
│      └── policy_impl.py
│
├── memory/
│      └── conversation_memory.py
│
├── models/
│      ├── request_model.py
│      └── response_model.py
│
├── prompts/
│      └── policy_prompt.py
│
├── routers/
│      └── policy_router.py
│
├── services/
│      └── policy_service.py
│
├── vectorstore/
│      └── vector_store.py
│
├── uploaded_documents/
│
├── chroma_db/
│
├── logs/
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

# Supported Documents

* Hospital SOPs
* HR Policies
* Nursing Policies
* Infection Control Guidelines
* Pharmacy Policies
* Compliance Manuals
* NABH Documents
* JCI Documents
* Quality Manuals
* Emergency Procedures

---

# Conversational RAG Flow

```
Upload Documents
        │
        ▼
Document Loader
        │
        ▼
Text Splitter
        │
        ▼
Embeddings
        │
        ▼
ChromaDB
        │
        ▼
Retriever
        │
        ▼
Conversation Memory
        │
        ▼
LLM
        │
        ▼
Answer with Sources
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Hospital_Policy_Assistant.git

cd Hospital_Policy_Assistant
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install fastapi
pip install uvicorn
pip install loguru

pip install langchain
pip install langchain-core
pip install langchain-community
pip install langchain-chroma
pip install langchain-huggingface
pip install langchain-ollama

pip install chromadb
pip install sentence-transformers

pip install pypdf
pip install docx2txt
```

---

# Run Ollama

Example:

```bash
ollama pull llama3.2

ollama serve
```

---

# Run the Application

```bash
uvicorn main:app --reload
```

---

# Swagger UI

```
http://localhost:8000/docs
```

---

# API Endpoints

## Upload Document

POST

```
/policy/upload
```

Supports

* PDF
* DOCX
* TXT

---

## Upload Multiple Documents

POST

```
/policy/upload-multiple
```

---

## Ask Question

POST

```
/policy/ask
```

Sample Request

```json
{
    "question":"What is the leave policy?",
    "language":"English",
    "user_id":"EMP001",
    "session_id":"SESSION001"
}
```

Sample Response

```json
{
  "success": true,
  "message": "Answer generated successfully.",
  "question": "What is the leave policy?",
  "answer": "Employees are entitled to 12 casual leaves per year...",
  "conversation_id": "SESSION001",
  "language": "English",
  "sources": [
    {
      "document_name": "HR_Policy.pdf",
      "page_number": 15,
      "section": "Leave Policy"
    }
  ]
}
```

---

## Clear Memory

DELETE

```
/policy/memory/{session_id}
```

---

## Health

GET

```
/policy/health
```

---

## Collection Statistics

GET

```
/policy/statistics
```

---

## Active Sessions

GET

```
/policy/sessions
```

---

## Reset Database

DELETE

```
/policy/database/reset
```

---

# Supported File Types

* PDF
* DOCX
* TXT

---

# Memory

The application maintains **session-based conversation memory**.

Each user session has independent chat history.

Example

```
User A
Session A

↓

Memory A

----------------------

User B
Session B

↓

Memory B
```

---

# Logging

Loguru provides:

* API Request Logs
* Document Upload Logs
* Vector Store Logs
* Memory Logs
* Errors
* Stack Traces

Log files are stored in

```
logs/
```

---

# Vector Database

* ChromaDB
* Persistent Storage
* Semantic Search
* Similarity Search
* Metadata Support

---

# Embedding Model

```
sentence-transformers/all-MiniLM-L6-v2
```

---

# Large Language Model

Default

```
llama3.2
```

Can be replaced with

* GPT-4
* GPT-4.1
* Mistral
* Gemma
* DeepSeek
* Qwen

---

# Future Enhancements

* Hybrid Search (BM25 + Vector Search)
* Metadata Filtering
* Role-Based Access Control (RBAC)
* Document Versioning
* Redis Memory
* PostgreSQL Metadata
* Streaming Responses
* JWT Authentication
* Docker Support
* Kubernetes Deployment
* Azure OpenAI Integration
* LangSmith Tracing
* Monitoring Dashboard

---

# Skills Demonstrated

* FastAPI
* LangChain
* Conversational RAG
* Retrieval-Augmented Generation
* ChromaDB
* HuggingFace Embeddings
* Ollama
* Prompt Engineering
* Session Memory
* Enterprise Logging
* REST API Development
* Modular Architecture

---

# License

This project is intended for educational and enterprise reference purposes. Choose an appropriate open-source license (such as MIT or Apache-2.0) if you plan to distribute it publicly.

---

# Author

Developed using **Python**, **LangChain**, **FastAPI**, and **ChromaDB** following enterprise software architecture and best practices.
