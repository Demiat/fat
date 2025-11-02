import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import insert, update, select
from sqlalchemy.exc import IntegrityError
from starlette import status

from fat.apps.auth.schemas import (
    CreateUserSchema, UserReturnDataSchema, GetUserWithIDAndEmailSchema
)
from fat.core.db_dependency import DBDependency
from fat.core.redis_dependency import RedisDependency
from fat.database.models import User

USER_EXISTS = "User already exists."


class UserManager:
    def __init__(
            self,
            db: DBDependency = Depends(DBDependency),
            redis: RedisDependency = Depends(RedisDependency),
    ) -> None:
        self.db = db
        self.model = User
        self.redis = redis

    async def create_user(
            self, user: CreateUserSchema) -> UserReturnDataSchema:
        async with self.db.db_session() as session:
            query = insert(
                self.model
            ).values(
                **user.model_dump()
            ).returning(
                self.model
            )
            try:
                result = await session.execute(query)
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=USER_EXISTS)
            await session.commit()
            user_data = result.scalar_one()
            return UserReturnDataSchema(**user_data.__dict__)

    async def confirm_user(self, email: str) -> None:
        async with self.db.db_session() as session:
            query = (
                update(self.model)
                .where(self.model.email == email)
                .values(is_verified=True, is_active=True)
            )
            await session.execute(query)
            await session.commit()

    async def get_user_by_email(
            self, email: str
    ) -> GetUserWithIDAndEmailSchema | None:
        async with self.db.db_session() as session:
            query = select(
                self.model.id,
                self.model.email,
                self.model.hashed_password
            ).where(self.model.email == email)

            result = await session.execute(query)
            # mappings() в SQLAlchemy используется для преобразования
            # результата запроса в словарь
            user = result.mappings().first()

            if user:
                return GetUserWithIDAndEmailSchema(**user)

            return None

    async def store_access_token(
            self, token: str, user_id: uuid.UUID, session_id: str
    ) -> None:
        async with self.redis.get_client() as client:
            await client.set(f"{user_id}:{session_id}", token)
