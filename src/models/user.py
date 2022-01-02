from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class User_login(BaseModel):
    user_hashed_password: str = Field(...)
    user_email: EmailStr = Field(...)


class User_create(BaseModel):
    """docstring for User_create."""
    user_name: str = Field(...)
    user_name_login: str = Field(..., min_length=5, max_length=20)
    user_email: EmailStr = Field(...)
    user_hashed_password: str = Field(..., min_length=5, max_length=200)
    user_is_active: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True


class User_base(User_create):
    """docstring for User_base."""
    user_id: int
