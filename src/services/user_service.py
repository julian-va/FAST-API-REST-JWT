from typing import List
from src.databases.config_db import get_db, Session
from fastapi import Depends
from src.mappers.user_mapper import User_mapper
from src.models.user import User_base, User_create
from src.entity_model.entitys import User_entity
from src.libs.utilities import Utilities


class User_service():
    """docstring for User_service."""

    def __init__(
            self, db: Session = Depends(get_db),
            user_mapper: User_mapper = Depends(User_mapper)):
        self._db = db
        self._user_mapper = user_mapper

    async def get_all_user(self) -> List[User_base]:

        try:
            result: List[User_base] = []
            temp = self._db.query(User_entity).all()

            if temp:
                result = await self._user_mapper.list_entity_to_list_pydantic(temp)

            return result
        except Exception as e:
            raise e

    async def create_user(self, user: User_create) -> User_base:

        try:
            password_temp = user.user_hashed_password
            user.user_hashed_password = await Utilities.encrypt_password(
                password_temp)
            temp = User_entity(**user.dict())
            self._db.add(temp)
            self._db.commit()
            self._db.refresh(temp)
            return await self._user_mapper.user_entity_to_user_pydantic(temp)

        except Exception as e:
            self._db.rollback()
            raise e

    def delete_user(self, user_id: int):
        try:
            result = self._db.query(User_entity).filter(
                User_entity.user_id == user_id).first()
            if result:
                self._db.delete(result)
                self._db.commit()
                return result

        except Exception as e:
            self._db.rollback()
            raise e

    async def update_user(self, user_id: int, user: User_create):
        try:
            str1: bytes = ""
            str2: bytes = ""
            temp = self._db.query(User_entity).filter(
                User_entity.user_id == user_id).first()

            if temp:
                temp.user_email = user.user_email
                str1 = temp.user_hashed_password
                str2 = user.user_hashed_password.encode()

                if str1 == str2:
                    temp.user_hashed_password == user.user_hashed_password
                else:
                    user.user_hashed_password = await Utilities.encrypt_password(
                        user.user_hashed_password)
                    temp.user_hashed_password = user.user_hashed_password

                temp.user_is_active = user.user_is_active
                temp.user_name = user.user_name
                temp.user_name_login = user.user_name_login
                self._db.commit()

                result = self._db.query(User_entity).filter(
                    User_entity.user_id == user_id).first()
                return await self._user_mapper.user_entity_to_user_pydantic(result)
            return None
        except Exception as e:
            self._db.rollback()
            raise e
