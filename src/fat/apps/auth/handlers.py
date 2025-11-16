from typing import NamedTuple
import datetime
import uuid

from passlib.context import CryptContext
from fastapi import HTTPException
from starlette import status
import jwt

from fat.core.settings import settings


class CreateTokenTuple(NamedTuple):
    encoded_jwt: str
    session_id: str


class AuthHandler:
    """
    Пользовательский обработчик аутентификации и безопасности.
    Устанавливаем класс как Синглтон.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Создаем новый объект и сохраняем в атрибут класса
            cls._instance = super().__new__(cls)
            cls._instance.secret = settings.secret_key.get_secret_value()
            cls._instance.pwd_context = CryptContext(
                schemes=["bcrypt"],
                # Eсли схема хэширования станет устаревшей,
                # passlib автоматически перейдёт на более современную.
                deprecated="auto"
            )
        return cls._instance

    async def get_password_hash(self, password: str) -> str:
        """Получает хэш пароля."""
        return self.pwd_context.hash(password)

    async def verify_password(
            self, raw_password: str, hashed_password: str) -> bool:
        """Проверяет пароль на соответствие хэшу."""
        return self.pwd_context.verify(raw_password, hashed_password)

    async def create_access_token(
        self, user_id: uuid.UUID
    ) -> CreateTokenTuple:
        """Создает access токен."""
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            seconds=settings.access_token_expire
        )
        session_id = str(uuid.uuid4())

        data = {
            "exp": expire,
            "session_id": session_id,
            "user_id": str(user_id)
        }

        encoded_jwt = jwt.encode(
            payload=data, key=self.secret, algorithm="HS256")

        return CreateTokenTuple(encoded_jwt=encoded_jwt, session_id=session_id)

    async def decode_access_token(self, token: str) -> dict:
        """Расшифровывает access токен."""
        try:
            return jwt.decode(jwt=token, key=self.secret, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired or Invalid token"
            )
