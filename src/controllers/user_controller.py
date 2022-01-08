from typing import List
from fastapi import APIRouter, status, Body, Depends
from fastapi.responses import JSONResponse
from src.models.user import User_create, User_base
from src.services.user_service import User_service
from src.middlewares.route_token_verify import Route_token_rerify

routes_users = APIRouter(prefix="/api/v1/users")
# route_class=Route_token_rerify)


@routes_users.post(path="/create", response_model=User_base, status_code=status.HTTP_201_CREATED, summary="Create a User", tags=["Users"])
async def create(user: User_create = Body(...), service: User_service = Depends(User_service)):
    try:
        user_create = await service.create_user(user)
        return user_create
    except Exception as e:
        raise e


@routes_users.get(path="/allUser", response_model=List[User_base], status_code=status.HTTP_200_OK, summary="get lla User", tags=["Users"])
def all_user(service: User_service = Depends(User_service)):
    try:
        user_all: User_base = service.get_all_user()
        return user_all
    except Exception as e:
        raise e


@routes_users.delete(path="/deleteUser/{user_id}", status_code=status.HTTP_200_OK | status.HTTP_404_NOT_FOUND, summary="delete User", tags=["Users"])
def delete_user(user_id: int, service: User_service = Depends(User_service)):
    try:
        user_delete = service.delete_user(user_id)
        if user_delete is None:
            return JSONResponse(content="User not found", status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=f"User Delete:[ user_id: {user_delete.user_id}, user_name_login: {user_delete.user_name_login}]", status_code=status.HTTP_200_OK)
    except Exception as e:
        raise e


@routes_users.put(path="/update/{user_id}", status_code=status.HTTP_200_OK | status.HTTP_404_NOT_FOUND, summary="delete User", tags=["Users"])
async def delete_user(user_id: int, user: User_base = Body(...), service: User_service = Depends(User_service)):
    try:
        user_updtae = await service.update_user(user_id, user)
        if user_updtae is None:
            return JSONResponse(content="User not found", status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=user_updtae.dict(), status_code=status.HTTP_200_OK)
    except Exception as e:
        raise e
