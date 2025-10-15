from app.core.config import SessionLocal
from app.db.model.chat_model import ChatHistory
from app.core.loadenv import Settings

def get_chat_history(user_id: int):
    db = SessionLocal()
    history = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(Settings.CHAT_HISTORY_LIMIT)
        .all()
    )
    db.close()
    # reverse to maintain chronological order
    history.reverse()
    return [{"user_prompt": h.user_prompt, "ai_response": h.ai_response} for h in history]

def save_chat(user_prompt: str, ai_response: str , user_id: int):
    db = SessionLocal()
    chat = ChatHistory(user_prompt=user_prompt, ai_response=ai_response, user_id=user_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    db.close()
    return chat
