from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from datetime import datetime
import uuid

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

VECTOR_STORE_PATH = "../faiss_index"

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def build_vector_store(data):
    """Build and save a FAISS vector store from knowledge base data."""
    docs = [
        Document(
            page_content=f"Q: {item['question']}\nA: {item['answer']}",
            metadata=item
        )
        for item in data
    ]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("../faiss_index")  # Save to parent directory
    return vectorstore

def load_vector_store():
    """Load a FAISS vector store from local storage."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.load_local("../faiss_index", embeddings, allow_dangerous_deserialization=True)  # Load from parent directory

def add_question_to_vector_store(item: dict, file_path=VECTOR_STORE_PATH):
    """
    Adds a new QA entry from knowledge base into FAISS vector store.
    The item must follow the knowledge base schema.
    """

    required_keys = {"question", "answer", "category", "audience", "tags", "created", "ticket_id"}
    if not required_keys.issubset(set(item.keys())):
        raise ValueError(f"Missing required keys in item: {required_keys - set(item.keys())}")

    # Load or initialize vector store
    if os.path.exists(file_path):
        vectorstore = FAISS.load_local(file_path, embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents([], embeddings)

    # Metadata
    ticket_id = item["ticket_id"]
    timestamp = datetime.now().isoformat()

    metadata = {
        "question": item["question"],
        "answer": item["answer"],
        "category": item["category"],
        "audience": item["audience"],
        "tags": item["tags"],
        "created": item["created"],
        "added_timestamp": timestamp,
        "ticket_id": ticket_id
    }

    # Build page content (embedding text)
    page_content = (
        f"Category: {item['category']}\n"
        f"Audience: {', '.join(item['audience'])}\n"
        f"Tags: {', '.join(item['tags'])}\n"
        f"Created: {item['created']}\n\n"
        f"Q: {item['question']}\nA: {item['answer']}"
    )

    doc = Document(page_content=page_content, metadata=metadata)
    vectorstore.add_documents([doc])
    vectorstore.save_local(file_path)

    return f"TICKET-{ticket_id}"