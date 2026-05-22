import json
import queue
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fastapi import Request
from fastapi.responses import StreamingResponse, JSONResponse
from database.models import Session, Chat
from database.share_variable import get_steps as _get_steps_from_dict
from database.share_variable import init_session, set_session_steps
from rag.generation.chat import ChatPipeline
from config.logger_config import setup_logger

logger = setup_logger("chat_service")

_pipeline: ChatPipeline = None
_pipeline_init_error: str | None = None

def _get_pipeline() -> ChatPipeline:
    global _pipeline, _pipeline_init_error
    if _pipeline is not None:
        return _pipeline
    if _pipeline_init_error is not None:
        raise RuntimeError(f"ChatPipeline 初始化失败（之前尝试已失败）: {_pipeline_init_error}")

    logger.info("初始化 ChatPipeline...")
    try:
        _pipeline = ChatPipeline()
        logger.info("ChatPipeline 初始化完成")
        return _pipeline
    except Exception as e:
        _pipeline_init_error = str(e)
        logger.error(f"ChatPipeline 初始化失败: {e}", exc_info=True)
        raise


async def chat(request: Request):
    """对话接口 —— 前端传入已有 session_id 进行对话"""
    body = await request.json()
    session_id = body.get("session_id")
    query = (body.get("query") or "").strip()

    logger.info(f"[session={session_id}] 收到对话请求: query={query[:80]}...")


    if not session_id or not query:
        logger.warning(f"[session={session_id}] 参数不完整: session_id={session_id}, query={query[:50] if query else 'None'}")
        return JSONResponse(status_code=400, content={"code": 400, "message": "session_id 和 query 不能为空"})

    session = await Session.filter(session_id=session_id, is_delete=False).first()
    if not session:
        logger.warning(f"[session={session_id}] 会话不存在")
        return JSONResponse(status_code=404, content={"code": 404, "message": "会话不存在"})

    logger.info(f"[session={session_id}] 会话有效, 准备流式响应")

    init_session(session_id)

    return StreamingResponse(
        _sse_generator(session_id, query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


async def _sse_generator(session_id: int, query: str):
    q: queue.Queue = queue.Queue()
    loop = asyncio.get_running_loop()
    records = await Chat.filter(
        session_id=session_id, is_delete=False
    ).order_by("-created_at").limit(30).all()
    records = list(reversed(records))
    history = [{"role": r.role, "content": r.chat_message} for r in records]
    logger.info(f"[session={session_id}] 加载历史消息: {len(history)} 条")

    def run_pipeline():
        collected = []
        steps = []
        try:
            pipeline = _get_pipeline()
            logger.info(f"[session={session_id}] 开始执行对话管道")
            for chunk in pipeline.chat(query, steps, history=history):
                collected.append(chunk)
                q.put(("chunk", chunk))
            full_response = "".join(collected)
            logger.info(f"[session={session_id}] 管道完成, AI回复长度={len(full_response)}")
            q.put(("done", full_response, steps))
        except Exception as e:
            logger.error(f"[session={session_id}] 管道执行异常: {e}", exc_info=True)
            q.put(("error", str(e)))
        q.put(("finish", None))

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(run_pipeline)
    logger.info(f"[session={session_id}] 管道线程已启动")

    try:
        while True:
            try:
                msg = await loop.run_in_executor(None, q.get, True, 0.05)
                msg_type = msg[0]
                if msg_type == "chunk":
                    yield f"data: {json.dumps({'type': 'chunk', 'content': msg[1]}, ensure_ascii=False)}\n\n"
                elif msg_type == "done":
                    content = msg[1]
                    pipe_steps = msg[2]
                    if content:
                        # 对话结束后统一保存：用户消息 + AI 消息
                        await Chat.create(session_id=session_id, role="user", chat_message=query)
                        await Chat.create(session_id=session_id, role="assistant", chat_message=content)
                        await Session.filter(session_id=session_id).update(created_at=datetime.now())
                        pipeline_steps = [f"加载历史消息: {len(history)} 条"] + pipe_steps
                        set_session_steps(session_id, pipeline_steps)
                        logger.info(f"[session={session_id}] 消息已持久化: user={query[:30]}..., ai_len={len(content)}")
                    else:
                        logger.warning(f"[session={session_id}] AI回复为空, 跳过持久化")
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                elif msg_type == "error":
                    logger.error(f"[session={session_id}] SSE错误: {msg[1]}")
                    yield f"data: {json.dumps({'type': 'error', 'message': msg[1]}, ensure_ascii=False)}\n\n"
                elif msg_type == "finish":
                    logger.info(f"[session={session_id}] SSE流结束")
                    break
            except queue.Empty:
                yield ": keepalive\n\n"
    except Exception as e:
        logger.error(f"[session={session_id}] SSE生成器异常: {e}", exc_info=True)
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"
    finally:
        executor.shutdown(wait=False)
        logger.debug(f"[session={session_id}] 线程池已关闭")



async def get_step(session_id: str):
    """通过session_id从共享字典中获取本次对话的完整步骤列表"""
    steps = _get_steps_from_dict(session_id)
    if steps is None:
        return JSONResponse(status_code=404, content={"code": 404, "message": "未找到该会话的步骤记录"})
    return JSONResponse(content={"code": 200, "data": {"session_id": session_id, "steps": steps}})