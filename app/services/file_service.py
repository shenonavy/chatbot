import os
import uuid
import shutil
from typing import List
from dto.file_response import UploadResponse, FileProcessResult
from fastapi import UploadFile
from core.logger import logging
from data import loader as document_loader
from data.database import vectorstore

TEMP_DIR = "temp/uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

def run_file_upload(files: List[UploadFile]) -> UploadResponse:
    response_data: list[FileProcessResult] = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            continue

        unique_filename = f"{uuid.uuid4()}.pdf"
        temp_path = os.path.join(TEMP_DIR, unique_filename)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            splitters = document_loader.doc_loader(temp_path)
            vectorstore.add_documents(splitters)

            response_data.append(FileProcessResult(
                original_filename=file.filename,
                chunks_count=len(splitters)
            ))

        except Exception as e:
            logging.exception(f"Error processing file {file.filename}")
            response_data.append(FileProcessResult(
                original_filename=file.filename,
                error=str(e)
            ))

        finally:
            os.remove(temp_path)

    return UploadResponse(
        message=f"{len(files)} file(s) uploaded and processed.",
        results=response_data
    )