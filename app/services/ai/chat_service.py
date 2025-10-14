from app.core.config import SessionLocal
from app.db.model.chat_model import ChatHistory

def get_chat_history(company_id: int , user_id:int):
    db = SessionLocal()
    history = db.query(ChatHistory).filter(ChatHistory.company_id == company_id , ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp).all()
    db.close()
    return [{"user_prompt": h.user_prompt, "ai_response": h.ai_response} for h in history]

def save_chat(company_id: int, user_prompt: str, ai_response: str , user_id: int):
    db = SessionLocal()
    chat = ChatHistory(company_id=company_id, user_prompt=user_prompt, ai_response=ai_response, user_id=user_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    db.close()
    return chat
