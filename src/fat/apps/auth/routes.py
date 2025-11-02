from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from fat.apps.auth.schemas import AuthUserSchema, UserReturnDataSchema
from fat.apps.auth.services import UserService

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


@auth_router.get(path="/register_confirm", status_code=status.HTTP_200_OK)
async def confirm_registration(
    token: str, service: UserService = Depends(UserService)
) -> dict[str, str]:
    """Подтверждение регистрации."""
    await service.confirm_user(token=token)
    return {"message": "Электронная почта подтверждена"}


@auth_router.post(path="/login", status_code=status.HTTP_200_OK)
async def login(
    user: AuthUserSchema, service: UserService = Depends(UserService)
) -> JSONResponse:
    """Аутентификация пользователя."""
    return await service.login_user(user=user)
