from typing import Optional
from pydantic import BaseModel

class FileProcessResult(BaseModel):
    original_filename: str
    chunks_count: Optional[int] = None
    error: Optional[str] = None

class UploadResponse(BaseModel):
    message: str
    results: list[FileProcessResult]
