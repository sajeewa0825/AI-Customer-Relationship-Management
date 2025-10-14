from fastapi import FastAPI
from app.core.config import engine
from app.db.model.document_model import Document
from app.db.model.chat_model import ChatHistory
from app.api.routes.documents.router import router as document_router
from app.api.routes.user.router import router as user_router
from app.db.create_vector_index import create_vector_index
import asyncio
from app.services.email.email_agent import auto_reply_agent

app = FastAPI()

async def background_email_checker():
    while True:
        try:
            auto_reply_agent()
        except Exception as e:
            print(f"⚠️ Error in email checker: {e}")
        await asyncio.sleep(300)  # check every 5 minute

@app.on_event("startup")
def startup_event():
    Document.metadata.create_all(bind=engine)
    ChatHistory.metadata.create_all(bind=engine)
    create_vector_index()
    asyncio.create_task(background_email_checker())

# Main route
app.include_router(document_router, prefix="/document", tags=["document"])
app.include_router(user_router, prefix="/user", tags=["user"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}