import os
import uuid
import asyncio
from datetime import datetime
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from database.models import Session, Chat, File
from rag.document_processing.parse import FileParserPipeline
from rag.document_processing.store import DocumentStorePipeline
from rag.generation.summarizer import DocumentSummarizer

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "uploads")

_parser: FileParserPipeline = None
_store_pipeline: DocumentStorePipeline = None
_summarizer: DocumentSummarizer = None


def _get_parser() -> FileParserPipeline:
    global _parser
    if _parser is None:
        _parser = FileParserPipeline()
    return _parser


def _get_store_pipeline() -> DocumentStorePipeline:
    global _store_pipeline
    if _store_pipeline is None:
        _store_pipeline = DocumentStorePipeline()
    return _store_pipeline


def _get_summarizer() -> DocumentSummarizer:
    global _summarizer
    if _summarizer is None:
        _summarizer = DocumentSummarizer()
    return _summarizer


def _save_to_disk(user_id: int, file: UploadFile) -> tuple[str, str]:
    """保存文件到磁盘，返回 (文件绝对路径, 原始文件名)"""
    original_name = file.filename
    ext = os.path.splitext(original_name)[1]
    saved_name = f"{uuid.uuid4().hex}{ext}"

    user_dir = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    target_path = os.path.abspath(os.path.join(user_dir, saved_name))

    return target_path, original_name


async def upload(user_id: int, session_id: int, file: UploadFile):
    """对话中的文件上传 —— 解析 → LLM摘要 → 存入对话历史"""
    if not file.filename:
        return JSONResponse(status_code=400, content={"code": 400, "message": "文件名为空"})

    session = await Session.filter(session_id=session_id, is_delete=False).first()
    if not session:
        return JSONResponse(status_code=404, content={"code": 404, "message": "会话不存在"})

    content = await file.read()
    target_path, original_name = _save_to_disk(user_id, file)

    def _write_file():
        with open(target_path, "wb") as f:
            f.write(content)

    await asyncio.to_thread(_write_file)

    docs = await asyncio.to_thread(_get_parser().parse_file, target_path)
    doc_text = "\n\n".join(d.page_content for d in docs) if docs else ""

    if len(doc_text) < 500:
        summary = doc_text
    else:
        summary = await asyncio.to_thread(_get_summarizer().summarize, doc_text, original_name)

    system_msg = f"[上传文件] {original_name}\n\n{summary}"
    chat_record = await Chat.create(session_id=session_id, role="fileupload", chat_message=system_msg)
    await Session.filter(session_id=session_id).update(created_at=datetime.now())

    record = await File.create(
        user_id=user_id,
        session_id=session_id,
        chat_id=chat_record.chat_id,
        file_name=original_name,
        source=target_path,
        is_rag=False,
    )

    return {
        "code": 200,
        "message": "上传并摘要成功",
        "data": {
            "file_id": record.file_id,
            "file_name": record.file_name,
            "source": record.source,
            "summary": summary,
        },
    }


async def upload_rag(user_id: int, file: UploadFile):
    """RAG知识库文件上传 —— 解析 → 切片 → 向量化 → 存入Milvus/ES"""
    if not file.filename:
        return JSONResponse(status_code=400, content={"code": 400, "message": "文件名为空"})

    content = await file.read()
    target_path, original_name = _save_to_disk(user_id, file)

    def _write_file():
        with open(target_path, "wb") as f:
            f.write(content)

    await asyncio.to_thread(_write_file)

    record = await File.create(
        user_id=user_id,
        file_name=original_name,
        source=target_path,
        is_rag=True,
    )

    result = await asyncio.to_thread(_get_store_pipeline().store, target_path)

    return {
        "code": 200,
        "message": "RAG文档入库成功",
        "data": {
            "file_id": record.file_id,
            "file_name": record.file_name,
            "source": record.source,
            "vector_count": result[0] if result else 0,
            "text_count": result[1] if result else 0,
        },
    }


async def delete_file(file_id: int):
    record = await File.filter(file_id=file_id, is_delete=False).first()
    if not record:
        return JSONResponse(status_code=404, content={"code": 404, "message": "文件不存在"})

    # 如果有chat_id，软删除对应的聊天消息
    if record.chat_id:
        await Chat.filter(chat_id=record.chat_id).update(is_delete=True)

    # 如果是RAG文件，删除向量数据库和ES中的文档
    if record.is_rag:
        await asyncio.to_thread(_get_store_pipeline().delete_by_file, record.source)

    record.is_delete = True
    await record.save()

    return {"code": 200, "message": "删除成功"}


async def get_history(user_id: int):
    files = await File.filter(user_id=user_id, is_delete=False).values(
        "file_id", "file_name", "session_id", "created_at"
    )

    for f in files:
        if f["created_at"]:
            f["created_at"] = f["created_at"].isoformat()

    return {
        "code": 200,
        "message": "获取成功",
        "data": files,
    }
