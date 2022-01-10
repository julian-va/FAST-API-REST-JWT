
from dataclasses import dataclass
import uuid
import os
from sqlalchemy.sql.expression import true
from src.libs.utilities import Utilities
from typing import List
from src.databases.config_db import get_db, Session
from fastapi import Depends, UploadFile
from src.mappers.user_files_mapper import User_files_mapper
from src.models.user_file import User_file_create, User_file_base
from src.entity_model.entitys import User_file_entity


@dataclass
class Files_service():
    """docstring for Files_service."""
    __path: str = os.getenv("UPLOAD_DIR")

    def __init__(self, db: Session = Depends(get_db),
                 user_files_mapper: User_files_mapper = Depends(User_files_mapper)):
        self._db = db
        self._user_files_mapper = user_files_mapper

    async def upload_file_list(self, user_id: int, files: List[UploadFile]) -> List[User_file_base]:
        result: List[User_file_base] = []
        dirs: List[str] = []
        path: str = os.getenv("UPLOAD_DIR")
        try:
            for file in files:
                name_file_dir: str = f"{path}user_id={user_id}-{uuid.uuid1()}-{file.filename}"
                with open(name_file_dir, "wb") as my_file:
                    content = await file.read()
                    my_file.write(content)
                    my_file.close()
                    user_file = User_file_entity()
                    user_file.user_file_dir = name_file_dir
                    user_file.user_file_name = file.filename
                    user_file.user_file_type = file.content_type
                    user_file.user_id = user_id
                    self._db.add(user_file)
                    self._db.flush()
                    dirs.append(user_file.user_file_dir)
            result = await self.get_files_user_id(user_id)

        except Exception as e:
            Utilities.delete_files(file_list_dir=dirs)
            self._db.rollback()
            raise e
        self._db.commit()
        return result

    async def get_files_user_id(self, user_id: int):
        try:
            result = self._db.query(User_file_entity).filter(
                User_file_entity.user_id == user_id).all()
            return await self._user_files_mapper.list_entity_to_list_pydantic(result)

        except Exception as e:
            raise e

    async def get_files_id(self, file_id: int) -> List[User_file_base]:
        result: List[User_file_base] = []
        try:
            temp = self._db.query(User_file_entity).filter(
                User_file_entity.user_file_id == file_id).first()

            if temp:
                result.append(await self._user_files_mapper.user_file_entity_to_user_pydantic(temp))

        except Exception as e:
            raise e
        return result

    async def get_all_files(self) -> List[User_file_base]:
        result: List[User_file_base] = []
        try:
            temp = self._db.query(User_file_entity).all()

            if temp:
                result = await self._user_files_mapper.list_entity_to_list_pydantic(temp)

        except Exception as e:
            raise e
        return result

    async def delete_files(self, file_id: int) -> List[User_file_base]:
        result: List[User_file_base] = []
        try:
            temp = self._db.query(User_file_entity).filter(
                User_file_entity.user_file_id == file_id).first()

            if temp:
                self._db.delete(temp)
                self._db.flush()
                result.append(await self._user_files_mapper.user_file_entity_to_user_pydantic(temp))
                Utilities.delete_files(file_dir=temp.user_file_dir)

        except Exception as e:
            self._db.rollback()
            raise e
        self._db.commit()
        return result

    async def delete_all_files(self):
        validate: bool = False
        try:
            results = await self.get_all_files()

            if results:
                validate = True
                for file in results:
                    temp = await self.delete_files(file.user_file_id)

        except Exception as e:
            raise e
        return validate
