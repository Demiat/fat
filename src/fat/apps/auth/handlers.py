from passlib.context import CryptContext
from fat.core.settings import settings


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
