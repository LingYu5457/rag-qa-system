from fastapi import APIRouter,Request
from database.models import User
from backend.app.user import user_service

user_router = APIRouter()

@user_router.post("/register")
async def register(request: Request):
    """用户注册"""
    return await user_service.register(request)

@user_router.post("/login")
async def login(request: Request):
    """用户登录"""
    return await user_service.login(request)