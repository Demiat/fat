from fastapi import Depends
from starlette.responses import JSONResponse

from fat.apps.auth.handlers import AuthHandler
from fat.apps.profile.managers import ProfileManager
from fat.apps.profile.schemas import ChangeEmailSchema, ChangePasswordSchema
from fat.database.models import User


class ProfileService:
    """
    Сервис для работы с данными профиля пользователя.
    """

    def __init__(
        self,
        manager: ProfileManager = Depends(ProfileManager),
        handler: AuthHandler = Depends(AuthHandler),
    ) -> None:
        """Создает экземпляр сервиса профиля с необходимыми зависимостями."""
        self.manager = manager
        self.handler = handler

    async def change_email(
            self,
            data: ChangeEmailSchema,
            user: User) -> None:
        """Обновляет адрес электронной почты пользователя."""
        return await self.manager.update_user_fields(
            user_id=user.id, email=data.new_email
        )

    async def change_password(
            self,
            data: ChangePasswordSchema,
            user: User) -> None | JSONResponse:
        """Изменяет пароль пользователя после проверки старого значения."""
        # Проверяем старый пароль
        if await self.handler.verify_password(
            raw_password=data.old_password,
            hashed_password=user.hashed_password
        ):
            # Получаем хэш по новому паролю
            hashed_password = await self.handler.get_password_hash(
                password=data.new_password
            )
            # Обновляем пароль
            await self.manager.update_user_fields(
                user_id=user.id,
                hashed_password=hashed_password
            )
            return None

        return JSONResponse({"detail": "Invalid password"}, status_code=401)
