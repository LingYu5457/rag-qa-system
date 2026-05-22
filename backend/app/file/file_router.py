from fastapi import APIRouter, UploadFile, File, Form
from backend.app.file import file_service

file_router = APIRouter()


@file_router.post("/upload")
async def upload(
    user_id: int = Form(...),
    session_id: int = Form(...),
    file: UploadFile = File(...),
):
    return await file_service.upload(user_id, session_id, file)


@file_router.post("/upload_rag")
async def upload_rag(
    user_id: int = Form(...),
    file: UploadFile = File(...),
):
    return await file_service.upload_rag(user_id, file)


@file_router.delete("/{file_id}")
async def delete_file(file_id: int):
    return await file_service.delete_file(file_id)


@file_router.get("/history/{user_id}")
async def get_history(user_id: int):
    return await file_service.get_history(user_id)
