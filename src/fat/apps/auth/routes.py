from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from fat.apps.auth.schemas import (
    AuthUserSchema, UserReturnDataSchema,
    UserVerifySchema, MessageResponseSchema
)
from fat.apps.auth.services import UserService
from fat.apps.auth.depends import get_current_user

# tags для группировки маршрутов в документации
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    response_model=UserReturnDataSchema,
    status_code=status.HTTP_201_CREATED
)
async def registration(
    user: AuthUserSchema,
    service: UserService = Depends(UserService)
) -> UserReturnDataSchema:
    """Регистрация пользователя."""
    return await service.register_user(user=user)


@auth_router.get(
    path="/register_confirm",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseSchema
)
async def confirm_registration(
    token: str,
    service: UserService = Depends(UserService)
) -> dict[str, str]:
    """Подтверждение регистрации."""
    await service.confirm_user(token=token)
    return {"message": "Электронная почта подтверждена"}


@auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseSchema
)
async def login(
    user: AuthUserSchema, service: UserService = Depends(UserService)
) -> JSONResponse:
    """Аутентификация пользователя."""
    return await service.login_user(user=user)


@auth_router.get(
    path="/logout",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseSchema
)
async def logout(
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: UserService = Depends(UserService),
) -> JSONResponse:
    """Выход пользователя: отзыв access токена."""
    return await service.logout_user(user=user)


@auth_router.get(
    path="/get-user",
    status_code=status.HTTP_200_OK,
    response_model=UserVerifySchema
)
async def get_auth_user(
    user: Annotated[UserVerifySchema, Depends(get_current_user)]
) -> UserVerifySchema:
    """Получить информацию о пользователе."""
    return user
