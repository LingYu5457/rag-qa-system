from fastapi import APIRouter, Request
from backend.app.chat import chat_service
from database import share_variable 

chat_router = APIRouter()

@chat_router.post("/query")
async def chat(request: Request):
    return await chat_service.chat(request)

@chat_router.get("/step/{session_id}")
async def get_step(session_id):
    return await chat_service.get_step(session_id)