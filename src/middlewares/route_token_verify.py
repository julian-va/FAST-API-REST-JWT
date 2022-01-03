from fastapi.routing import APIRoute
from fastapi import Request, status
from src.libs.jwt_functions import Jwt_methods
from fastapi.responses import JSONResponse


class Route_token_rerify(APIRoute):
    """docstring for Route_token_rerify."""

    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middlewares(resquest: Request):

            try:
                if resquest.headers.get("Authorization") != None:
                    token: str = resquest.headers["Authorization"].split(" ")[
                        1]
                    validate_response = Jwt_methods.token_validate(
                        token, outpul=False)
                    if validate_response == None:
                        return await original_route(resquest)
                    else:
                        return validate_response
                else:
                    return JSONResponse(content={"message": "Not Bearer Token"}, status_code=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                raise e

        return verify_token_middlewares
