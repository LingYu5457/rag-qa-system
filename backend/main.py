from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import fastapi_cdn_host
from tortoise.contrib.fastapi import register_tortoise
from config.settings import tortoise_settings
from backend.app.user import user_router
from backend.app.session import session_router
from backend.app.chat import chat_router
from backend.app.file import file_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router,prefix="/user",tags=["用户管理"])
app.include_router(session_router,prefix="/session",tags=["会话管理"])
app.include_router(chat_router,prefix="/chat",tags=["聊天"])
app.include_router(file_router,prefix="/file",tags=["文件管理"])

register_tortoise(
    app=app, 
    config=tortoise_settings.TORTOISE_CONFIG
)

fastapi_cdn_host.patch_docs(app)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)