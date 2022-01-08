
from dataclasses import dataclass
from typing import List
from src.databases.config_db import get_db, Session
from fastapi import Depends, UploadFile
from src.mappers.user_files_mapper import User_files_mapper
from src.models.user_file import User_file_create, User_file_base
from src.entity_model.entitys import User_file_entity
import os


@dataclass
class Files_service():
    """docstring for Files_service."""

    def __init__(self, db: Session = Depends(get_db),
                 user_files_mapper: User_files_mapper = Depends(User_files_mapper)):
        self._db = db
        self._user_files_mapper = user_files_mapper

    async def upload_file_list(self, user_id: int, files: List[UploadFile]) -> User_file_base:
        try:
            path: str = os.getenv("UPLOAD_DIR")
            if os.path.isdir(path) == False:
                os.mkdir(path)

            for file in files:
                with open(path+file.filename, "wb") as my_file:
                    content = await file.read()
                    my_file.write(content)
                    my_file.close()
                    user_file = User_file_entity()
                    user_file.user_file_dir = path+"/"+file.filename
                    user_file.user_file_name = file.filename
                    user_file.user_file_type = file.content_type
                    user_file.user_id = user_id
                    self._db.add(user_file)
                    self._db.commit()
                    self._db.refresh(user_file)
            return await self.get_files_user_id(user_id)

        except Exception as e:
            self._db.rollback()
            raise e

    async def get_files_user_id(self, user_id: int):
        try:
            result = self._db.query(User_file_entity).filter(
                User_file_entity.user_id == user_id).all()
            return await self._user_files_mapper.list_entity_to_list_pydantic(result)

        except Exception as e:
            raise e
