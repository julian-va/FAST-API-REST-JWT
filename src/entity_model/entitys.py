from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from src.databases.config_db import Base
from datetime import datetime


class User_entity(Base):
    """entity databesa"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(256), unique=False, index=True, nullable=False)
    user_name_login = Column(String(256), unique=True,
                             index=True, nullable=False)
    user_email = Column(String(256), unique=True, index=True, nullable=False)
    user_hashed_password = Column(String(256), nullable=False)
    user_is_active = Column(Boolean, default=False, nullable=False)
    creation_date = Column(DateTime(timezone=True),
                           default=datetime.now(), nullable=False)
    files_users = relationship("User_file_entity", back_populates="users")


class User_file_entity(Base):
    """entity User_file"""
    __tablename__ = "user_files"

    user_file_id = Column(Integer, primary_key=True, index=True)

    user_file_name = Column(String(256), unique=False,
                            index=True, nullable=False)
    user_file_dir = Column(String(256), unique=False,
                           index=True, nullable=False)
    user_file_type = Column(String(256), unique=False,
                            index=True, nullable=False)
    user_is_active = Column(Boolean, default=False, nullable=False)
    creation_date = Column(DateTime(timezone=True),
                           default=datetime.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    users = relationship(
        "User_entity", back_populates="files_users")
