from typing import List
from fastapi import UploadFile, File, Form, APIRouter, Depends, status, responses
from fastapi.responses import FileResponse, JSONResponse
from src.models.user_file import User_file_base
from src.services.files_service import Files_service

routes_files = APIRouter(prefix="/api/v1/files", tags=["files"])


@routes_files.post(path="/uploadMultipleFiles/{user_id}", response_model=List[User_file_base], status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(user_id: int, files: List[UploadFile] = File(...), service: Files_service = Depends(Files_service)):
    try:
        result = await service.upload_file_list(user_id, files)
        return result
    except Exception as e:
        raise e


@routes_files.get(path="/getfile/{file_id}", summary="you get the file saved by id")
async def get_file_id(file_id: int, service: Files_service = Depends(Files_service)):
    result = await service.get_files_id(file_id)
    if result:
        return FileResponse(result[0].user_file_dir)
    else:
        return JSONResponse(
            content={"file not Found"}, status_code=status.HTTP_404_NOT_FOUND)


@routes_files.get(path="/downloadFile/{file_id}", summary="you get the file saved by id")
async def download_file(file_id: int, service: Files_service = Depends(Files_service)):
    result = await service.get_files_id(file_id)
    if result:
        return FileResponse(result[0].user_file_dir, media_type="application/octet-stream", filename=result[0].user_file_name)
    else:
        return JSONResponse(
            content={"file not Found"}, status_code=status.HTTP_404_NOT_FOUND)


@routes_files.get(path="/getAllFile", response_model=List[User_file_base], status_code=status.HTTP_200_OK, summary="get all files")
async def get_all_files(service: Files_service = Depends(Files_service)):
    try:
        return await service.get_all_files()
    except Exception as e:
        raise e


@routes_files.delete(path="/deleteFile/{file_id}", status_code=status.HTTP_200_OK | status.HTTP_404_NOT_FOUND, summary="delete file")
async def delete_file(file_id: int, service: Files_service = Depends(Files_service)):
    try:
        result = await service.delete_files(file_id)
        if result:
            return JSONResponse(content=result[0].dict(),
                                status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(
                content=("file not Found"), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise e


@routes_files.delete(path="/deleteAllFiles", status_code=status.HTTP_200_OK | status.HTTP_404_NOT_FOUND, summary="delete all files")
async def delete_all_files(service: Files_service = Depends(Files_service)):
    try:
        result = await service.delete_all_files()
        if result:
            return JSONResponse(content=("all files have been deleted"),
                                status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(
                content=("There are no files to delete"), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise e
