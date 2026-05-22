import hashlib
import os
from fastapi import Request
from fastapi.responses import JSONResponse
from database.models import User


def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """使用PBKDF2-SHA256对密码进行哈希加密，返回(哈希值, 盐值)"""
    if salt is None:
        salt = os.urandom(32).hex()
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return hashed.hex(), salt


async def register(request: Request):
    """用户注册"""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"code": 400, "message": "请求体格式错误"})

    user_name = body.get("user_name", "").strip()
    user_account = body.get("user_account", "").strip()
    user_password = body.get("user_password", "").strip()

    if not user_name or not user_account or not user_password:
        return JSONResponse(status_code=400, content={"code": 400, "message": "用户名、账号、密码不能为空"})

    if len(user_name) > 50 or len(user_account) > 50 or len(user_password) > 255:
        return JSONResponse(status_code=400, content={"code": 400, "message": "字段长度超出限制"})

    existing = await User.filter(user_account=user_account, is_delete=False).first()
    if existing:
        return JSONResponse(status_code=409, content={"code": 409, "message": "账号已存在"})

    password_hash, salt = _hash_password(user_password)
    user = await User.create(
        user_name=user_name,
        user_account=user_account,
        user_password=f"{salt}${password_hash}"
    )

    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_account": user.user_account,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }


async def login(request: Request):
    """用户登录"""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"code": 400, "message": "请求体格式错误"})

    user_account = body.get("user_account", "").strip()
    user_password = body.get("user_password", "").strip()

    if not user_account or not user_password:
        return JSONResponse(status_code=400, content={"code": 400, "message": "账号和密码不能为空"})

    user = await User.filter(user_account=user_account, is_delete=False).first()
    if not user:
        return JSONResponse(status_code=401, content={"code": 401, "message": "账号或密码错误"})

    stored = user.user_password
    try:
        salt, stored_hash = stored.split("$", 1)
    except ValueError:
        return JSONResponse(status_code=500, content={"code": 500, "message": "密码存储格式错误"})

    computed_hash, _ = _hash_password(user_password, salt)
    if computed_hash != stored_hash:
        return JSONResponse(status_code=401, content={"code": 401, "message": "账号或密码错误"})

    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_account": user.user_account,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }
