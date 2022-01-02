from sqlalchemy import Boolean, Column, Integer, String
from src.databases.config_db import Base


class User_entity(Base):
    """entity databesa"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=False, index=True, nullable=False)
    user_name_login = Column(String, unique=True, index=True, nullable=False)
    user_email = Column(String, unique=True, index=True, nullable=False)
    user_hashed_password = Column(String, nullable=False)
    user_is_active = Column(Boolean, default=True, nullable=False)
