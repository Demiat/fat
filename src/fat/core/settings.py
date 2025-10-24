from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """Настройки для подключения базы данных."""

    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    db_echo: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_password.get_secret_value()}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )


class EmailSettings(BaseSettings):
    email_host: str
    email_port: int
    email_username: str
    email_password: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore")


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class Settings(BaseSettings):
    """Совокупный класс настроек."""

    db_settings: DBSettings = DBSettings()
    email_settings: EmailSettings = EmailSettings()
    redis_settings: RedisSettings = RedisSettings()
    secret_key: SecretStr
    templates_dir: str = "tempaltes"
    frontend_url: str
    access_token_expire: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore")


settings = Settings()
