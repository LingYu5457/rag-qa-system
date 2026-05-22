from fastapi import APIRouter,Request
from backend.app.session import session_service


session_router = APIRouter()

@session_router.post("/create")
async def create_session(request: Request):
    return await session_service.create_session(request)
@session_router.get("/history/{user_id}")
async def get_session(user_id: int):
    """获取用户会话历史列表(包含会话id、标题和创建时间)"""
    return await session_service.get_session(user_id)

@session_router.get("/{session_id}")
async def get_session_detail(session_id: int):
    """获取用户会话详情(单次会话的所有消息列表，包括消息id、role、内容、创建时间)"""
    return await session_service.get_session_detail(session_id)

@session_router.delete("/{session_id}")
async def delete_session(session_id: int):
    """删除用户会话(逻辑删除，联合删除会话下的所有消息)"""
    return await session_service.delete_session(session_id)