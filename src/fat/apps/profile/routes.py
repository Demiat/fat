from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from fat.apps.auth.depends import get_current_user
from fat.apps.auth.schemas import UserVerifySchema
from fat.apps.profile.schemas import ChangeEmailSchema, ChangePasswordSchema
from fat.apps.profile.services import ProfileService

profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.post("/change-email", status_code=status.HTTP_200_OK)
async def change_email(
    data: ChangeEmailSchema,
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: ProfileService = Depends(ProfileService),
) -> None:
    """Изменяет адрес электронной почты текущего пользователя."""
    return await service.change_email(data=data, user=user)


@profile_router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    data: ChangePasswordSchema,
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: ProfileService = Depends(ProfileService),
) -> Response:
    """Обновляет пароль авторизованного пользователя."""
    return await service.change_password(data=data, user=user)
