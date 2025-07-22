from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

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