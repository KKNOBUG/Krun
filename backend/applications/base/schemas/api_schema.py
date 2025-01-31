# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : api_schema.py
@DateTime: 2025/1/31 17:36
"""
from typing import Optional

from pydantic import BaseModel, Field


class ApiCreate(BaseModel):
    path: str = Field(example="/getAccessToken")
    method: str = Field(example="POST")
    summary: str = Field(example="Base-用户鉴权")
    tags: str = Field(example="基础服务")
    is_active: Optional[bool] = True

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class ApiUpdate(BaseModel):
    id: int
    path: Optional[str] = None
    method: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[str] = None
    is_active: Optional[bool] = True
