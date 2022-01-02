from fastapi import APIRouter, status, Body, Depends
from src.models.user import User_login
from src.services.auth_service import Auth_service
from fastapi.responses import JSONResponse

routes_auth = APIRouter(prefix="/api/v1/auth")


@routes_auth.post(path="/login", summary="Login a User", tags=["Auth"])
async def login(user: User_login = Body(...), service: Auth_service = Depends(Auth_service)):
    try:
        result = await service.login_verification(user.user_hashed_password, user.user_email)
        if result:
            return JSONResponse(content=f"{result}", status_code=status.HTTP_202_ACCEPTED)
        return JSONResponse(content=f"{result}", status_code=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        raise e
    print(user)
