from fastapi.responses import JSONResponse
from database.models import Session, Chat, File
from rag.generation.title_generator import TitleGenerator
from rag.document_processing.store import DocumentStorePipeline
import asyncio
from fastapi import Request
from config.logger_config import setup_logger

logger = setup_logger("session_service")

_title_generator: TitleGenerator = None

def _get_title_generator() -> TitleGenerator:
    global _title_generator
    if _title_generator is None:
        logger.info("初始化 TitleGenerator...")
        _title_generator = TitleGenerator()
        logger.info("TitleGenerator 初始化完成")
    return _title_generator

async def create_session(request: Request):
    """创建新会话，由 LLM 生成标题，返回 session_id 和标题"""
    body = await request.json()
    user_id = body.get("user_id")
    query = (body.get("query") or "").strip()

    logger.info(f"[user={user_id}] 创建会话请求: query={query[:80]}...")

    if not user_id:
        logger.warning("创建会话失败: user_id 为空")
        return JSONResponse(status_code=400, content={"code": 400, "message": "user_id 不能为空"})
    if not query:
        logger.warning(f"[user={user_id}] 创建会话失败: query 为空")
        return JSONResponse(status_code=400, content={"code": 400, "message": "query 不能为空"})

    try:
        title = await asyncio.to_thread(_get_title_generator().generate, query)
        logger.info(f"[user={user_id}] 标题生成: {title}")
    except Exception as e:
        logger.error(f"[user={user_id}] 标题生成失败: {e}", exc_info=True)
        title = query[:20]  # fallback

    session = await Session.create(user_id=user_id, session_title=title)
    logger.info(f"[user={user_id}] 会话创建成功: session_id={session.session_id}, title={title}")

    return {
        "code": 200,
        "message": "创建成功",
        "data": {
            "session_id": session.session_id,
            "session_title": title,
        },
    }


async def get_session(user_id: int):
    """获取用户会话历史列表（含会话ID、标题和创建时间）"""
    logger.info(f"[user={user_id}] 查询会话历史")

    sessions = await Session.filter(user_id=user_id, is_delete=False).values(
        "session_id", "session_title", "created_at"
    )

    for s in sessions:
        if s["created_at"]:
            s["created_at"] = s["created_at"].isoformat()

    logger.info(f"[user={user_id}] 会话历史: {len(sessions)} 条")

    return {
        "code": 200,
        "message": "获取成功",
        "data": sessions
    }


async def get_session_detail(session_id: int):
    """获取单次会话的所有消息（含消息ID、role、内容、创建时间）"""
    logger.info(f"[session={session_id}] 查询会话详情")

    session = await Session.filter(session_id=session_id, is_delete=False).first()
    if not session:
        logger.warning(f"[session={session_id}] 会话不存在")
        return JSONResponse(status_code=404, content={"code": 404, "message": "会话不存在"})

    chats = await Chat.filter(session_id=session_id, is_delete=False).order_by("created_at").values(
        "chat_id", "role", "chat_message", "created_at"
    )

    for c in chats:
        if c["created_at"]:
            c["created_at"] = c["created_at"].isoformat()

    logger.info(f"[session={session_id}] 会话详情: {len(chats)} 条消息")

    return {
        "code": 200,
        "message": "获取成功",
        "data": {
            "session_id": session.session_id,
            "session_title": session.session_title,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "chats": chats
        }
    }


_store_pipeline: DocumentStorePipeline = None


def _get_store() -> DocumentStorePipeline:
    global _store_pipeline
    if _store_pipeline is None:
        _store_pipeline = DocumentStorePipeline()
    return _store_pipeline


async def delete_session(session_id: int):
    """逻辑删除会话，同时删除关联的消息和文件"""
    logger.info(f"[session={session_id}] 删除会话")

    session = await Session.filter(session_id=session_id, is_delete=False).first()
    if not session:
        logger.warning(f"[session={session_id}] 会话不存在，无法删除")
        return JSONResponse(status_code=404, content={"code": 404, "message": "会话不存在"})

    session.is_delete = True
    await session.save()

    # 软删除所有聊天消息
    await Chat.filter(session_id=session_id, is_delete=False).update(is_delete=True)

    # 处理该会话下的所有文件
    files = await File.filter(session_id=session_id, is_delete=False).all()

    # 先删除RAG向量/ES数据
    rag_files = [f for f in files if f.is_rag]
    if rag_files:
        store = _get_store()
        for f in rag_files:
            await asyncio.to_thread(store.delete_by_file, f.source)

    # 再软删除所有文件
    await File.filter(session_id=session_id, is_delete=False).update(is_delete=True)

    logger.info(f"[session={session_id}] 会话已删除，关联文件数: {len(files)}, RAG文件数: {len(rag_files)}")

    return {
        "code": 200,
        "message": "删除成功"
    }
