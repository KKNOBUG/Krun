# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : department_schema.py
@DateTime: 2025/2/3 16:27
"""
from typing import Optional

from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    code: str = Field(example="DT-CS01", description="部门代码")
    name: str = Field(example="测试一部", description="部门名称")
    description: Optional[str] = Field(default=None, example="测试部门，测试一部", description="部门描述")
    order: int = Field(default=0, example=0, description="排序")
    parent_id: int = Field(default=0, example=0, description="父部门ID")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class DepartmentUpdate(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    order: int = 0
    parent_id: int = 0
    updated_user: Optional[str] = None

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class DepartmentSelect(BaseModel):
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=10, description="数据数量")
    order: Optional[list] = Field(default=["id"], description="排序字段")
    created_user: Optional[str] = None
    updated_user: Optional[str] = None
    created_time: Optional[str] = None
    updated_time: Optional[str] = None
