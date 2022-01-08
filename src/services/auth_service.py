from src.libs.utilities import Utilities
from src.databases.config_db import get_db, Session
from src.entity_model.entitys import User_entity
from fastapi import Depends


class Auth_service():
    """docstring for Auth_service."""

    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    async def login_verification(self, password: str, user_email: str) -> bool:
        try:
            verification: bool = False
            result: User_entity = self._db.query(User_entity).filter(
                User_entity.user_email == user_email).first()

            if result:
                verification = await Utilities.compare_password(password, result.user_hashed_password)

            return verification
        except Exception as e:
            raise e
