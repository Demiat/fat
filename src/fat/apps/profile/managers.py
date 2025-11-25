import uuid
from typing import Any

from fastapi import Depends
from sqlalchemy import update

from fat.core.db_dependency import DBDependency
from fat.database.models import User


class ProfileManager:
    """
    Менеджер для работы с данными профиля в базе данных.
    """

    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        """Инициализирует менеджер с зависимостью доступа к базе данных."""
        self.db = db
        self.user_model = User

    async def update_user_fields(
            self, user_id: uuid.UUID | str, **kwargs: Any) -> None:
        """Обновляет выбранные поля пользователя по его идентификатору."""
        async with self.db.db_session() as session:
            query = update(self.user_model).where(
                self.user_model.id == user_id).values(**kwargs)

            await session.execute(query)

            await session.commit()

    # async def get_user_hashed_password(self, user_id: uuid.UUID | str) -> str:
    #     """Возвращает хешированный пароль пользователя."""
    #     async with self.db.db_session() as session:
    #         query = select(self.user_model.hashed_password).where(
    #             self.user_model.id == user_id)

    #         result = await session.execute(query)

    #         return result.scalar()
