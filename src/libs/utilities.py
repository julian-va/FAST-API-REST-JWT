from bcrypt import gensalt, hashpw, checkpw


class Utilities(object):
    """docstring for Utilities,
    contains helper methods"""

    @staticmethod
    async def encrypt_password(password: str) -> bytes:
        try:

            salt: bytes = gensalt(rounds=20,)
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
