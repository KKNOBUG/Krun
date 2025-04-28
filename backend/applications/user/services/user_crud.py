# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : user_crud.py
@DateTime: 2025/1/18 11:36
"""
from datetime import datetime
from typing import Optional, Union, List

from tortoise.exceptions import DoesNotExist

from backend.applications.base.schemas.token_schema import CredentialsSchema
from backend.applications.base.services.role_crud import ROLE_CRUD
from backend.applications.user.models.user_model import User
from backend.applications.user.schemas.user_schema import UserCreate, UserUpdate
from backend.core.exceptions.base_exceptions import NotFoundException, BaseExceptions, DataAlreadyExistsException
from backend.core.responses.http_response import ForbiddenResponse
from backend.services.password import verify_password, get_password_hash
from backend.applications.base.services.scaffold import ScaffoldCrud


class UserCrud(ScaffoldCrud[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.model.filter(id=user_id).first()

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.filter(username=username).first()

    async def get_by_alias(self, username: str) -> Optional[List[User]]:
        return await self.model.filter(username=username).all()

    async def authenticate(self, credentials: CredentialsSchema) -> Optional[Union[BaseExceptions, User]]:
        user = await self.model.filter(username=credentials.username).first()
        if not user:
            raise NotFoundException(message="用户名不存在")
        verified = verify_password(credentials.password, user.password)
        if not verified:
            raise NotFoundException(message="用户名或密码错误")
        if user.state in (0, 4):
            raise NotFoundException(message="用户待岗或已离职")
        return user

    async def update_last_login(self, id: int) -> None:
        user = await self.model.get(id=id)
        user.last_login = datetime.now()
        await user.save()

    async def create_user(self, user_in: UserCreate) -> User:
        email = user_in.email
        username = user_in.username
        instances = await self.model.filter(email=email, username=username).all()
        if instances:
            raise DataAlreadyExistsException(message=f"用户(email={email},username={username})信息已存在")

        user_in.password = get_password_hash(password=user_in.password)
        instance = await self.create(user_in)
        await self.update_roles(instance, user_in.role_ids)
        return instance

    async def delete_user(self, user_id: int) -> User:
        instance = await self.query(user_id)
        if not instance:
            raise NotFoundException(message=f"用户(id={user_id})信息不存在")

        instance.state = 0
        instance.is_active = 0
        await instance.save()
        return instance

    async def update_user(self, user_in: UserUpdate) -> User:
        user_id: int = user_in.id
        user_if: dict = {
            key: value for key, value in user_in.items()
            if value is not None
        }
        try:
            instance = await self.update(id=user_id, obj_in=user_if)
        except DoesNotExist as e:
            raise NotFoundException(message=f"用户(id={user_id})信息不存在")

        data = await instance.to_dict()
        return data

    @classmethod
    async def update_roles(cls, user: User, role_ids: List[int]) -> None:
        await user.roles.clear()
        for role_id in role_ids:
            role_obj = await ROLE_CRUD.get(id=role_id)
            await user.roles.add(role_obj)

    async def reset_password(self, user_id: int):
        instance = await self.get(id=user_id)
        if instance.is_superuser:
            return ForbiddenResponse(message="不允许重置超级用户密码")

        instance.password = get_password_hash(password="123456")
        await instance.save()
        data = await instance.to_dict(exclude_fields=["id", "password"])
        return data


USER_CRUD = UserCrud()
