from fastapi import APIRouter
from app.api.routes.user import chat_routes

router = APIRouter()
router.include_router(chat_routes.router)



