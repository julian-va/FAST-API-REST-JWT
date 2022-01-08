from typing import List
from fastapi import UploadFile, File, Form, APIRouter, Depends, status
from src.models.user_file import User_file_base
from src.services.files_service import Files_service

routes_files = APIRouter(prefix="/api/v1/files")


@routes_files.post(path="/multiple/files/{user_id}", response_model=List[User_file_base], status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(user_id: int, files: List[UploadFile] = File(...), service: Files_service = Depends(Files_service)):
    try:
        result = await service.upload_file_list(user_id, files)
        return result
    except Exception as e:
        raise e
