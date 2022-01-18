
import this
from src.libs.utilities import Utilities
from src.databases.config_db import get_db, Session
from src.entity_model.entitys import User_entity
from fastapi import Depends
from src.mappers.user_mapper import User_mapper


class Auth_service():
    """docstring for Auth_service."""

    def __init__(self, db: Session = Depends(get_db), maper_user: User_mapper = Depends(User_mapper)):
        self._db = db
        self._user_mapper = maper_user

    async def login_verification(self, password: str, user_email: str):
        try:
            verification: bool = False
            result: User_entity = self._db.query(User_entity).filter(
                User_entity.user_email == user_email).first()

            if result:
                verification = await Utilities.compare_password(password, result.user_hashed_password)
                if verification:
                    return verification, await self._user_mapper.user_entity_to_user_pydantic(result)

            return verification
        except Exception as e:
            raise e
