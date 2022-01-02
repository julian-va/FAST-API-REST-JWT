from os import getenv
from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi import status


class Jwt_methods:

    @staticmethod
    def write_token(data: dict, days: int) -> str:
        try:
            date: datetime = datetime.now()
            new_date: datetime = date + timedelta(days)
            token: str = encode(
                payload={**data, "exp": new_date}, key=getenv("SECRET"), algorithm="HS256")
            return token
        except Exception as e:
            raise e

    @staticmethod
    def token_validate(token: str, outpul: bool = False):
        try:
            if outpul:
                decode(token, key=getenv("SECRET"), algorithms=["HS256"])
            decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        except exceptions.DecodeError as e:
            return JSONResponse(content={"message": "Invalid Token"}, status_code=status.HTTP_401_UNAUTHORIZED)
        except exceptions.ExpiredSignatureError as e:
            return JSONResponse(content={"message": "Invalid Expired"}, status_code=status.HTTP_401_UNAUTHORIZED)
