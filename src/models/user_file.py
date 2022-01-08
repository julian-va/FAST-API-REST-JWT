from typing import Optional
from pydantic import BaseModel, Field


class User_file_create(BaseModel):
    """docstring for User_create."""
    user_file_name: str = Field(...)
    user_file_dir: str = Field(...)
    user_file_type: str = Field(...)
    user_is_active: Optional[bool] = Field(default=False)
    user_id: int = Field(...)

    class Config:
        orm_mode = True


class User_file_base(User_file_create):
    """docstring for User_create."""
    user_file_id: int = Field(...)

    class Config:
        orm_mode = True
