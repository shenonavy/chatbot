from fastapi import APIRouter, Request, UploadFile, File
from typing import List
from services.file_service import run_file_upload

router = APIRouter()

@router.post("/upload")
async def Upload(files: List[UploadFile] = File(...)):
    return run_file_upload(files)