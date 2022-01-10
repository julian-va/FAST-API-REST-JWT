from dataclasses import dataclass
from typing import List
from src.entity_model.entitys import User_entity
from src.models.user import User_base


@dataclass
class User_mapper():
    """Docstring for User_mapper."""
    async def user_entity_to_user_pydantic(self, user: User_entity) -> User_base:
        try:
            result: User_base = User_base(
                user_email=user.user_email,
                user_hashed_password=user.user_hashed_password,
                user_id=user.user_id,
                user_is_active=user.user_is_active,
                user_name=user.user_name,
                user_name_login=user.user_name_login,
                creation_date=user.creation_date)
            return result
        except Exception as e:
            raise e

    async def list_entity_to_list_pydantic(self, list_user_entity: List[User_entity]) -> List[User_base]:
        try:
            result: List[User_base] = []
            for user_entity in list_user_entity:
                result2 = await self.user_entity_to_user_pydantic(user_entity)
                result.append(result2)
            return result
        except Exception as e:
            raise e
