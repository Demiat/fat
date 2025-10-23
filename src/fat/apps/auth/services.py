from fastapi import Depends
from fastapi import HTTPException
from itsdangerous import BadSignature, URLSafeTimedSerializer

from fat.apps.auth.handlers import AuthHandler
from fat.apps.auth.managers import UserManager
from fat.apps.auth.schemas import (
    RegisterUserSchema, UserReturnDataSchema, CreateUserSchema)
from fat.apps.auth.tasks import send_confirmation_email
from fat.core.settings import settings


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
            self, user: RegisterUserSchema) -> UserReturnDataSchema:
        hashed_password = await self.handler.get_password_hash(user.password)

        new_user = CreateUserSchema(
            email=user.email, hashed_password=hashed_password)

        user_data = await self.manager.create_user(user=new_user)

        confirmation_token = self.serializer.dumps(user_data.email)
        send_confirmation_email.delay(
            to_email=user_data.email, token=confirmation_token)

        return user_data

    async def confirm_user(self, token: str) -> None:
        try:
            email = self.serializer.loads(token, max_age=3600)
        except BadSignature:
            raise HTTPException(
                status_code=400, detail="Неверный или просроченный токен"
            )

        await self.manager.confirm_user(email=email)
