# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : scene_group_model.py
@DateTime: 2025/3/8 19:08
"""
from tortoise import fields

from backend.applications.base.services.scaffold import (
    ScaffoldModel,
    StateModel,
    MaintainMixin,
    TimestampMixin
)


class SceneGroup(ScaffoldModel, StateModel, MaintainMixin, TimestampMixin):
    code = fields.CharField(max_length=16, unique=True, description="模块代码")
    name = fields.CharField(max_length=64, unique=True, description="模块名称")
    description = fields.TextField(null=True, description="模块描述")

    class Meta:
        table = "krun_scene_group"
