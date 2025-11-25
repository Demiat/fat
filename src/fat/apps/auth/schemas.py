import uuid
import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints


class GetUserByIDSchema(BaseModel):
    id: uuid.UUID | str


class GetUserByEmailSchema(BaseModel):
    email: EmailStr


class AuthUserSchema(GetUserByEmailSchema):
    password: Annotated[str, StringConstraints(min_length=8, max_length=128)]


class CreateUserSchema(GetUserByEmailSchema):
    hashed_password: str


class UserReturnDataSchema(GetUserByIDSchema, GetUserByEmailSchema):
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class GetUserWithIDAndEmailSchema(GetUserByIDSchema, CreateUserSchema):
    pass


# class UserVerifySchema(GetUserByIDSchema, GetUserByEmailSchema):
#     session_id: uuid.UUID | str | None = None


class FullUserReturnDataSchema(UserReturnDataSchema):
    session_id: uuid.UUID | str | None = None


class MessageResponseSchema(BaseModel):
    message: str


class ErrorResponseSchema(BaseModel):
    detail: str


# class UserIDEmailSessionHashSchema(UserVerifySchema):
#     hashed_password: str

#     class Config:
#         from_attributes = True
