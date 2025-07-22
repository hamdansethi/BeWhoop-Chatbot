from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from ticket_manager import save_unanswered_question_v2

def initialize_llm():
    """Initialize the LLM and prompt template as a RunnableSequence."""
    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template="""
You are a helpful assistant answering questions about account creation, vendors, event details, etc.

Question: {question}
Knowledge Base Info: {context}

Respond appropriately:
- If the question is relevant and has a matching answer, return it.
- If it's relevant but not answerable, reply "NO_ANSWER" (this triggers ticket creation).
- If it's irrelevant, reply "IRRELEVANT".
"""
    )
    return prompt | llm

def find_relevant_docs(query, vectorstore):
    """Find relevant documents in the vector store."""
    results = vectorstore.similarity_search_with_relevance_scores(query, k=10)
    return results[0][0] if results else None

async def handle_user_question(user_input, vectorstore, user_contact=None):
    """Handle user questions and return appropriate responses."""
    llm_chain = initialize_llm()
    
    relevant_doc = find_relevant_docs(user_input, vectorstore)
    context = relevant_doc.page_content if relevant_doc else "None"

    if not relevant_doc or context.strip().lower() in ["none", ""]:
        user_contact = user_contact or {"email": None, "whatsapp": None}
        ticket_id = save_unanswered_question_v2(user_input, user_contact)
        return {
            "response": f"Thanks! I couldn’t find an answer, but I’ve created a ticket for you: {ticket_id}. Our team will reach out soon.",
            "ticket_id": ticket_id
        }

    llm_response = await llm_chain.ainvoke({"question": user_input, "context": context})
    response_text = llm_response.content.strip()

    if response_text == "IRRELEVANT":
        return {
            "response": "I'm only trained to help with things like account creation, vendors, and events. Please try asking something like that.",
            "ticket_id": None
        }

    elif response_text == "NO_ANSWER":
        user_contact = user_contact or {"email": None, "whatsapp": None}
        ticket_id = save_unanswered_question_v2(user_input, user_contact)
        return {
            "response": f"Thanks! We’ve created a ticket for you: {ticket_id}. Our team will get back to you soon.",
            "ticket_id": ticket_id
        }

    return {
        "response": response_text,
        "ticket_id": None
    }

def handle_user_question_sync(user_input, vectorstore):
    """Synchronous wrapper for CLI compatibility."""
    import asyncio
    return asyncio.run(handle_user_question(user_input, vectorstore))