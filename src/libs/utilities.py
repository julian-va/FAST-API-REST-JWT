from typing import List
from bcrypt import gensalt, hashpw, checkpw
import os


class Utilities():
    """docstring for Utilities,
    contains helper methods"""

    @staticmethod
    async def encrypt_password(password: str) -> bytes:
        try:

            salt: bytes = gensalt(rounds=10,)
            hashed: bytes = hashpw(password.encode(), salt)
            return hashed
        except Exception as e:
            raise e

    @staticmethod
    async def compare_password(password: str, hashed_password: bytes) -> bool:
        try:
            password_validation: bool = False
            password_validation = checkpw(password.encode(), hashed_password)
            return password_validation
        except Exception as e:
            raise e

    @staticmethod
    def create_folders() -> None:
        try:
            path: str = os.getenv("UPLOAD_DIR")
            if os.path.isdir(path) == False:
                os.mkdir(path)
        except Exception as e:
            raise e

    @staticmethod
    def delete_files(file_dir: str = None, file_list_dir: List[str] = None) -> None:
        try:
            if file_dir != None:
                if os.path.isfile(file_dir):
                    os.remove(file_dir)

            if file_list_dir != None:
                for dir in file_list_dir:
                    if os.path.isfile(dir):
                        os.remove(dir)
        except Exception as e:
            raise e
