from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from ticket_manager import save_unanswered_question_individual

def initialize_llm():
    """Initialize the LLM and prompt template as a RunnableSequence."""
    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template="""You are a helpful assistant for BeWhoop services. 
Answer questions related to account creation, vendor information, events, etc.

Question: {question}
Knowledge Base: {context}

Instructions:
- If the context provides an answer, give it clearly and concisely.
- If the context is related but doesn’t directly answer, return ONLY "NO_ANSWER".
- If the question is not related at all, return ONLY "IRRELEVANT".
"""
    )
    return prompt | llm

def find_relevant_docs(query, vectorstore):
    """Find the most relevant document in the vector store."""
    results = vectorstore.similarity_search_with_relevance_scores(query, k=1)
    if results and results[0][1] >= 0.6:  # You can adjust threshold
        return results[0][0]
    return None

async def handle_user_question(user_input, vectorstore, user_contact=None):
    """Main async handler to process a user question."""
    llm_chain = initialize_llm()
    doc = find_relevant_docs(user_input, vectorstore)
    context = doc.page_content if doc else ""

    # Call LLM with or without context
    llm_response = await llm_chain.ainvoke({
        "question": user_input,
        "context": context if context.strip() else "None"
    })

    reply = llm_response.content.strip()

    # Case: irrelevant
    if reply.upper() == "IRRELEVANT":
        return {
            "response": "I'm here to help with questions about accounts, vendors, and events. Try asking something like that.",
            "ticket_id": None
        }

    # Case: relevant but no answer → Create ticket
    if reply.upper() == "NO_ANSWER":
        ticket_id = save_unanswered_question_individual(user_input, user_contact or {})
        return {
            "response": f"Thanks! I couldn’t find an answer, but I’ve created a ticket for you: {ticket_id}. Our team will reach out soon.",
            "ticket_id": ticket_id
        }

    # Case: proper answer found
    return {
        "response": reply,
        "ticket_id": None
    }

def handle_user_question_sync(user_input, vectorstore, user_contact=None):
    """Sync wrapper for CLI or non-async environments."""
    import asyncio
    return asyncio.run(handle_user_question(user_input, vectorstore, user_contact))
