from fastapi import APIRouter

from api.routes import (
    user_router,
    chat_router,
    session_router,
    messages_router,
    auth_router,
)


api_router = APIRouter()
api_router.include_router(user_router.router)
api_router.include_router(chat_router.router)
api_router.include_router(session_router.router)
api_router.include_router(messages_router.router)
api_router.include_router(auth_router.router)

