from langchain_groq import ChatGroq
from app.core.config import Settings
from app.services.embedding.embedding_service import retrieve_company_context

def run_rag_query(company_id: int, user_prompt: str, history: list, system_prompt: str):
    # Step 1: Get relevant company context
    context = retrieve_company_context(company_id, user_prompt)

    # Step 2: Initialize Groq LLM
    llm = ChatGroq(
        model=Settings.MODEL_NAME,
        temperature=Settings.TEMPERATURE,
        max_tokens=Settings.MAX_TOKENS,
        api_key=Settings.GROQ_API_KEY
    )

    # Step 3: Build conversational context
    messages = [
        ("system", f"{system_prompt}:\n{context}"),
    ]
    for msg in history:
        messages.append(("human", msg["user_prompt"]))
        messages.append(("ai", msg["ai_response"]))
    messages.append(("human", user_prompt))

    # Step 4: Run the model
    ai_message = llm.invoke(messages)
    return ai_message.content
