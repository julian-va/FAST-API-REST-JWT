from os import getenv
from fastapi import APIRouter, status, Body, Depends, Header
from src.models.user import User_base, User_login
from src.services.auth_service import Auth_service
from fastapi.responses import JSONResponse
from src.libs.jwt_functions import Jwt_methods
from fastapi.security import OAuth2PasswordBearer

routes_auth = APIRouter(prefix="/api/v1/auth")

oauth_2passwor = OAuth2PasswordBearer("/api/v1/auth/login")


@routes_auth.post(path="/login", summary="Login a User", tags=["Auth"])
async def login(user: User_login = Body(...), service: Auth_service = Depends(Auth_service)):
    try:
        result: tuple = await service.login_verification(user.user_hashed_password, user.user_email)
        if result:
            user: User_base = result[1]
            user.creation_date = None
            token = Jwt_methods.write_token(
                user.dict(), int(getenv("TOKEN_DURATION")))
            return JSONResponse(content={"token": f"{token}"}, status_code=status.HTTP_202_ACCEPTED)
        return JSONResponse(content={"message": "invalid email or password"}, status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        raise e


@routes_auth.post(path="/token/verify", summary="verify token", tags=["Auth"])
async def token_verify(Authorization: str = Header(default=None)):
    if Authorization != None:
        token = Authorization.split(" ")[1]
        return Jwt_methods.token_validate(token, outpul=True)
    return JSONResponse(content={"message": "Not token authorization"}, status_code=status.HTTP_404_NOT_FOUND)
