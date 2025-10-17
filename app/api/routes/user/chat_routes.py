from fastapi import APIRouter, status, HTTPException
from app.db.schema.chat_schema import ChatCreate, ChatResponse
from app.services.ai.chat_service import get_chat_history, save_chat
from app.services.ai.rag_service import run_rag_query
from app.services.filter.filter_service import classify_message

router = APIRouter()

@router.post("/chat",  status_code=status.HTTP_201_CREATED)
async def chat_with_rag(request: ChatCreate):

    if request.user_id is None:
        raise HTTPException(status_code=400, detail="User ID required")
    if request.prompt is None:
        raise HTTPException(status_code=400, detail="Prompt Is required")
    
    # Load existing history
    history = get_chat_history( request.user_id)
    # print(f"Chat history: {history}")

    system_prompt ="You are an assistant for context data given company. Use the following context. also use previous chat history. important if can  get answer from the tools you must answer"
    # Generate response using RAG
    filter  = classify_message("api", request.prompt)
    print(f"Classified message category: {filter.category}")
    if filter.category in ["inquiry", "payment", "status", "order", "complaint"]:
        system_prompt += " to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer. and say Company agent will contact you soon."
    else:
        system_prompt += ". If you don't know the answer, just say that you don't know, don't try to make up an answer"
    ai_response = await run_rag_query(request.prompt, history , system_prompt )

    # Save to DB
    chat = save_chat( request.prompt, ai_response , request.user_id)

    return chat
