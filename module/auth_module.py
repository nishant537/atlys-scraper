from distutils.log import debug
from email import message
from http.client import responses
from telnetlib import STATUS
from urllib import response
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.database import *
from model.auth_model import GenerateTokenSchema
from crud.auth_crud import generate_token
import auth
from fastapi.security.api_key import APIKeyHeader
from auth import middleware_wrapper
from starlette.middleware import Middleware

# router = APIRouter(dependencies=[Depends(auth.get_api_key)])
router = APIRouter(
    route_class=middleware_wrapper(
        middleware=[
            Middleware(auth.CoreAccessMiddleware, header_value="test")
        ]
    ),
    dependencies=[Depends(APIKeyHeader(name="token"))],
)

@router.post('/')
async def create_token(payload:GenerateTokenSchema,db: Session = Depends(get_db), role = Depends(auth.admin_check_role)):
    return await generate_token(db, payload)

@router.get('/')
async def get_user(request: Request):
    return request.state.user
