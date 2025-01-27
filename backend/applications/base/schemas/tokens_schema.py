# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : tokens_schema.py
@DateTime: 2025/1/18 12:07
"""
from datetime import datetime

from pydantic import BaseModel, Field


class CredentialsSchema(BaseModel):
    username: str = Field(..., description="用户账号[电子邮箱或手机号码]", example="admin@test.com")
    password: str = Field(..., description="用户密码[a-zZ-Z0-9_-.*@!]", example="admin@123456")


class JWTOut(BaseModel):
    access_token: str
    username: str


class JWTPayload(BaseModel):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
