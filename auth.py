# auth.py
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Response, Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.types import ASGIApp
from typing import List, Optional, Type
from fastapi.routing import APIRoute
from html_response_codes import *
import os
from dotenv import load_dotenv

load_dotenv()

api_key_header = APIKeyHeader(name="token", auto_error=False)
APITOKEN = os.getenv('TOKEN')


# async def get_api_key(api_key_header: str = Security(api_key_header)):
#     if api_key_header == APITOKEN:
#         return api_key_header   
#     else:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=ErrorResponseModel(401, 'Unauthorized Access'))


# bind the middleware to an APIRoute subclass
def middleware_wrapper(middleware: Optional[List[Middleware]] = None) -> Type[APIRoute]:
    class CustomAPIRoute(APIRoute):
        def __init__(self, *args, **kwargs):
            super(CustomAPIRoute, self).__init__(*args, **kwargs)
            app = self.app
            for cls, options in reversed(middleware or []):
                app = cls(app, **options)
            self.app = app

    return CustomAPIRoute


async def admin_check_role(request: Request):
    if request.state.user["role"] != "admin":
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail={"message": 'Unauthorized Access'})


