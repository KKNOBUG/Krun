# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : http_exceptions.py
@DateTime: 2025/1/17 22:30
"""
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.exceptions import HTTPException
from tortoise.exceptions import DoesNotExist

from backend.core.response.base_response import BaseResponse
from backend.core.response.http_response import (
    ParameterResponse,
    ForbiddenResponse,
    NotFoundResponse,
    MethodNotAllowedResponse,
    RequestTimeoutResponse,
    LimiterResponse,
    InternalErrorResponse,
    BadGatewayResponse,
    GatewayTimeoutResponse,
    FailureResponse,
)


# 请求参数验证错误异常封装
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> BaseResponse:
    error_message: str = ""
    for error in exc.errors():
        error_message += ".".join(error.get("loc")) + ":" + error.get("msg") + " "

    return ParameterResponse(message=error_message.strip())


async def response_validation_exception_handler(request: Request, exc: ResponseValidationError) -> BaseResponse:
    error_message: str = ""
    for error in exc.errors():
        error_message += ".".join(map(str, error.get("loc"))) + ":" + error.get("msg") + " "

    return ParameterResponse(message=error_message.strip())


# 数据库空指针异常封装
async def null_point_exception_handler(request: Request, exc: DoesNotExist) -> BaseResponse:
    message: str = f'空指针异常：{exc.__str__()}'
    return NotFoundResponse(message=message.replace('"', "'"))


# HTTP请求异常封装
async def http_exception_handler(request: Request, exc: HTTPException) -> BaseResponse:
    if exc.status_code == status.HTTP_403_FORBIDDEN:
        return ForbiddenResponse(message=f"请求服务 {request.method} 未被授权")

    elif exc.status_code == status.HTTP_404_NOT_FOUND:
        return NotFoundResponse(message=f"请求资源 {request.url.path} 不可访达")

    elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        return MethodNotAllowedResponse(message=f"请求方式 {request.method} 不被允许")

    elif exc.status_code == status.HTTP_408_REQUEST_TIMEOUT:
        return RequestTimeoutResponse(message=f"请求数据 {request.method} 等待超时")

    elif exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        return LimiterResponse(message=f"请求速度 {request.method} 不被允许")

    elif exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        return InternalErrorResponse()

    elif exc.status_code == status.HTTP_502_BAD_GATEWAY:
        return BadGatewayResponse()

    elif exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        return GatewayTimeoutResponse()

    else:
        return FailureResponse(message=str(exc))


async def app_exception_handler(request: Request, exc: Exception) -> BaseResponse:
    return FailureResponse(message="服务器发生未知错误，请稍后重试，或点击右上角加入答疑群")
