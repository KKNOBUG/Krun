# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : token_view.py
@DateTime: 2025/1/18 10:03
"""
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter

from backend import PROJECT_CONFIG
from backend.applications.base.schemas.tokens_schema import CredentialsSchema, JWTOut, JWTPayload
from backend.applications.users.models.user_model import User
from backend.applications.users.services.user_crud import USER_CRUD
from backend.core.exceptions.base_exceptions import NotFoundException
from backend.core.response.base_response import (
    SuccessResponse,
    FailureResponse,
)
from backend.services.password import create_access_token

base = APIRouter()


@base.post("/getAccessToken", summary="base-获取鉴权")
async def get_login_access_token(credentials: CredentialsSchema):
    try:
        user: User = await USER_CRUD.authenticate(credentials)
    except NotFoundException as e:
        return FailureResponse(data=str(e))

    await USER_CRUD.update_last_login(user.id)
    access_token_expires = timedelta(minutes=PROJECT_CONFIG.AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    data = JWTOut(
        access_token=create_access_token(
            data=JWTPayload(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser,
                exp=expire,
            )
        ),
        username=user.username,
    )
    return SuccessResponse(data=data.model_dump())
