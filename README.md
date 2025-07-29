# BeWhoop Bot

**BeWhoop Bot** is a Python-based application that provides an intelligent query-handling system for questions related to account creation, vendors, and event details. It supports two interfaces: a command-line interface (CLI) for interactive use and an API for programmatic access. The system leverages LangChain with Google Generative AI for natural language processing and FAISS for vector-based similarity search to retrieve relevant answers from a knowledge base.

---

## Directory Structure

```
BeWhoop/
│
├── CLI/                        # CLI implementation and core modules
│   ├── main.py                 # CLI/API mode selector
│   ├── knowledge_base.py       # Loads the knowledge base
│   ├── vector_store.py         # FAISS vector store management
│   ├── ticket_manager.py       # Ticket creation for unanswered queries
│   └── query_handler.py        # LangChain-based query processor
│
├── API/                        # API implementation
│   └── main.py                 # FastAPI application
│
├── faiss_index/                # Stores FAISS vector index
│
├── bewhoop_kb.json             # Knowledge base (Q&A)
├── .env                        # Google API key environment file
├── unanswered_kb.json          # Unanswered questions (version 1)
├── unanswered_questions_v2.json# Unanswered questions (version 2)
└── requirements.txt            # Python dependencies
```

---

## Prerequisites

* Python 3.8 or higher
* Virtual environment (recommended)
* Google Generative AI API key

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd BeWhoop
```

### 2. Create and Activate a Virtual Environment

#### On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your API key:

```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Prepare the Knowledge Base

Ensure `bewhoop_kb.json` exists in the project root. This file should contain the relevant question-answer pairs for the knowledge base.

---

## Usage

### CLI Mode

To run the CLI interface:

```bash
cd CLI
python main.py --mode cli
```

This will allow you to enter queries interactively. Type `exit` or `quit` to stop the session.

### API Mode

You can start the FastAPI server in two ways:

**Option 1: From the CLI directory**

```bash
cd CLI
python main.py --mode api
```

**Option 2: From the API directory**

```bash
cd API
python main.py
```

Once running, the API will be available at `http://localhost:8001`.

---

## API Endpoints

### GET `/health`

Check if the server is running:

```bash
curl http://localhost:8001/health
```

**Response:**

```json
{"status": "healthy"}
```

---

### POST `/query`

Submit a user query along with optional contact details:

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "User Account Creation?", "email": "user@example.com", "whatsapp": "+1234567890"}'
```

You can also explore and test the endpoints through the Swagger UI at:

```
http://localhost:8001/docs
```
