BeWhoop Bot
Overview
BeWhoop Bot is a Python-based application that provides an intelligent query-handling system for questions related to account creation, vendors, and event details. It supports two interfaces: a command-line interface (CLI) for interactive use and an API for programmatic access. The system uses LangChain with Google Generative AI for natural language processing and FAISS for vector-based similarity search to retrieve relevant answers from a knowledge base.
Directory Structure

CLI/: Contains the CLI implementation and core modules.
main.py: Entry point for CLI and API mode selection.
knowledge_base.py: Handles loading the knowledge base.
vector_store.py: Manages FAISS vector store creation and loading.
ticket_manager.py: Manages ticket creation for unanswered questions.
query_handler.py: Processes user queries using LangChain.


API/: Contains the API implementation.
main.py: FastAPI application for API endpoints.


faiss_index/: Stores the FAISS vector index.
bewhoop_kb.json: Knowledge base JSON file.
.env: Environment file for Google API key.
unanswered_kb.json: Stores unanswered questions (version 1).
unanswered_questions_v2.json: Stores unanswered questions (version 2).

Prerequisites

Python 3.8 or higher
Virtual environment (recommended)
Google Generative AI API key

Setup

Clone the Repository:
git clone <repository-url>
cd BeWhoop


Create and Activate Virtual Environment:
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux


Install Dependencies:
pip install -r requirements.txt


Configure Environment:Create a .env file in the project root with:
GOOGLE_API_KEY=your_api_key_here


Prepare Knowledge Base:Ensure bewhoop_kb.json exists in the project root. This file contains the question-answer pairs for the knowledge base.


Usage
CLI Mode
Run the CLI interface from the CLI directory:
cd CLI
python main.py --mode cli

Enter queries interactively. Type exit or quit to stop.
API Mode
Run the FastAPI server from the CLI directory:
cd CLI
python main.py --mode api

Or directly from the API directory:
cd API
python main.py

The API will be available at http://localhost:8001.
API Endpoints

GET /health: Check server status.curl http://localhost:8001/health

Response: {"status": "healthy"}
POST /query: Submit a query with optional contact details.curl -X POST http://localhost:8001/query \
-H "Content-Type: application/json" \
-d '{"question": "User Account Creation?", "email": "user@example.com", "whatsapp": "+1234567890"}'

Explore endpoints via Swagger UI at http://localhost:8001/docs.
