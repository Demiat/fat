from fastapi import APIRouter, Depends
from starlette import status

from fat.apps.auth.schemas import RegisterUserSchema, UserReturnDataSchema
from fat.apps.auth.services import UserService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    response_model=UserReturnDataSchema,
    status_code=status.HTTP_201_CREATED
)
async def registration(
    user: RegisterUserSchema,
    service: UserService = Depends(UserService)
) -> UserReturnDataSchema:
    return await service.register_user(user=user)


@auth_router.get(path="/register_confirm", status_code=status.HTTP_200_OK)
async def confirm_registration(
    token: str, service: UserService = Depends(UserService)
) -> dict[str, str]:
    await service.confirm_user(token=token)
    return {"message": "Электронная почта подтверждена"}
