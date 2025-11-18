"""
URLSafeTimedSerializer - создает временный токен с
сериализованными данными.
"""

from fastapi import Depends
from fastapi import HTTPException
from itsdangerous import BadSignature, URLSafeTimedSerializer
from starlette import status
from starlette.responses import JSONResponse

from fat.apps.auth.handlers import AuthHandler
from fat.apps.auth.managers import UserManager
from fat.apps.auth.schemas import (
    AuthUserSchema, UserReturnDataSchema, CreateUserSchema, UserVerifySchema)
from fat.apps.auth.tasks import send_confirmation_email
from fat.core.settings import settings

BAD_TOKEN = "Неверный или просроченный токен!"


class UserService:
    def __init__(
            self,
            manager: UserManager = Depends(UserManager),
            handler: AuthHandler = Depends(AuthHandler)
    ):
        self.manager = manager
        self.handler = handler
        self.serializer = URLSafeTimedSerializer(
            secret_key=settings.secret_key.get_secret_value())

    async def register_user(
            self, user: AuthUserSchema) -> UserReturnDataSchema:
        """Создает пользователя и высылает подтверждающий токен."""
        hashed_password = await self.handler.get_password_hash(user.password)

        new_user = CreateUserSchema(
            email=user.email, hashed_password=hashed_password)

        user_data = await self.manager.create_user(user=new_user)

        confirmation_token = self.serializer.dumps(user_data.email)
        print(confirmation_token)
        send_confirmation_email.delay(
            to_email=user_data.email, token=confirmation_token)

        return user_data

    async def confirm_user(self, token: str) -> None:
        """Подтверждает пользователя из токена подтверждения."""
        try:
            email = self.serializer.loads(token, max_age=3600)
        except BadSignature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=BAD_TOKEN
            )

        await self.manager.confirm_user(email=email)

    async def login_user(self, user: AuthUserSchema) -> JSONResponse:
        """Создает access токен и помещает его в cookie."""
        exist_user = await self.manager.get_user_by_email(email=user.email)

        if exist_user is None or not await self.handler.verify_password(
            hashed_password=exist_user.hashed_password,
            raw_password=user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong email or password"
            )

        # Создаем access токен
        token, session_id = await self.handler.create_access_token(
            user_id=exist_user.id)

        # Сохраняем access токен в Redis
        await self.manager.store_access_token(
            token=token,
            user_id=exist_user.id,
            session_id=session_id
        )

        response = JSONResponse(content={"message": "Вход успешен"})
        response.set_cookie(
            key="Authorization",
            value=token,
            httponly=True,
            max_age=settings.access_token_expire,
        )

        return response

    async def logout_user(self, user: UserVerifySchema) -> JSONResponse:
        """Отзывает access токен."""
        await self.manager.revoke_access_token(
            user_id=user.id, session_id=user.session_id
        )

        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(key="Authorization")

        return response
