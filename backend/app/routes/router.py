from fastapi import APIRouter

from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.reminders import router as reminders_router
from app.routes.search import router as search_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(upload_router)
api_router.include_router(chat_router)
api_router.include_router(reminders_router)
api_router.include_router(search_router)
