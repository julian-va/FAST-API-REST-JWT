from dataclasses import dataclass
from typing import List
from src.entity_model.entitys import User_file_entity
from src.models.user_file import User_file_base


@dataclass()
class User_files_mapper(object):

    async def user_file_entity_to_user_pydantic(self, user_file_entity: User_file_entity) -> User_file_base:
        try:
            result: User_file_base = User_file_base(
                user_file_dir=user_file_entity.user_file_dir,
                user_file_name=user_file_entity.user_file_name,
                user_file_id=user_file_entity.user_file_id,
                user_file_type=user_file_entity.user_file_type,
                user_id=user_file_entity.user_id,
                user_is_active=user_file_entity.user_is_active
            )
            return result
        except Exception as e:
            raise e

    async def list_entity_to_list_pydantic(self, list_user_file_entity: List[User_file_entity]) -> List[User_file_base]:
        try:
            result: List[User_file_base] = []
            for user_file in list_user_file_entity:
                result_2 = await self.user_file_entity_to_user_pydantic(user_file)
                result.append(result_2)
            return result
        except Exception as e:
            raise e
