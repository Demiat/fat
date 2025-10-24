from fastapi import Depends, HTTPException
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from starlette import status

from fat.apps.auth.schemas import CreateUserSchema, UserReturnDataSchema
from fat.core.db_dependency import DBDependency
from fat.database.models import User

USER_EXISTS = "User already exists."

class UserManager:
    def __init__(self, db: DBDependency = Depends(DBDependency)) -> None:
        self.db = db
        self.model = User

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
