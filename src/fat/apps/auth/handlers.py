from typing import NamedTuple
import datetime
import uuid

from passlib.context import CryptContext
import jwt

from fat.core.settings import settings


class CreateTokenTuple(NamedTuple):
    encoded_jwt: str
    session_id: str


class AuthHandler:
    """Пользовательский обработчик аутентификации и безопасности."""

    secret = settings.secret_key.get_secret_value()
    pwd_context = CryptContext(
        schemes=["bcrypt"],

        # Eсли схема хэширования станет устаревшей,
        # passlib автоматически перейдёт на более современную.
        deprecated="auto"
    )

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(
            self, raw_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(raw_password, hashed_password)

    async def create_access_token(
        self, user_id: uuid.UUID
    ) -> CreateTokenTuple:
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
