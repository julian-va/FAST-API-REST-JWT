from typing import List
from src.databases.config_db import get_db, Session
from fastapi import Depends
from src.models.user import User_create
from src.entity_model.login_entity import User_entity
from src.libs.utilities import Utilities


class User_service():
    """docstring for User_service."""

    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def get_all_user(self) -> List[User_entity]:
        try:
            result = self._db.query(User_entity).all()
            return result
        except Exception as e:
            raise e

    async def create_user(self, user: User_create):
        try:
            password_temp = user.user_hashed_password
            user.user_hashed_password = await Utilities.encrypt_password(
                password_temp)

            temp = User_entity(**user.dict())
            self._db.add(temp)
            self._db.commit()
            self._db.refresh(temp)
            return temp
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
