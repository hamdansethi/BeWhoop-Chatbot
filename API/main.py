from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
import logging
from CLI.knowledge_base import load_knowledge_base
from CLI.vector_store import build_vector_store
from CLI.query_handler import handle_user_question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BeWhoop Bot API", description="API for BeWhoop Bot to handle user queries")

class QueryRequest(BaseModel):
    question: str
    email: str | None = None
    whatsapp: str | None = None

class QueryResponse(BaseModel):
    response: str
    ticket_id: str | None

def setup_environment():
    """Set up the environment by loading the Google API key from .env file."""
    logger.info("Loading .env file")
    load_dotenv(dotenv_path="../.env")
    if not os.environ.get("GOOGLE_API_KEY"):
        logger.error("GOOGLE_API_KEY not found in .env file")
        raise ValueError("GOOGLE_API_KEY not found in .env file")

# Initialize vector store at startup
logger.info("Initializing vector store")
setup_environment()
logger.info("Loading knowledge base")
kb_data = load_knowledge_base("../bewhoop_kb.json")
logger.info("Building vector store")
vectorstore = build_vector_store(kb_data)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a user query and return the response or ticket ID."""
    try:
        logger.info(f"Processing query: {request.question}")
        user_contact = {"email": request.email, "whatsapp": request.whatsapp}
        result = await handle_user_question(request.question, vectorstore, user_contact)
        logger.info(f"Query response: {result['response']}")
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

def run_api():
    """Run the FastAPI application."""
    logger.info("Starting FastAPI server")
    uvicorn.run(app, host="localhost", port=8001)

if __name__ == "__main__":
    run_api()