from fastapi import APIRouter

from fat.apps.auth.routes import auth_router
from fat.apps.profile.routes import profile_router

apps_router = APIRouter(prefix="/api/v1")

# Подключаем маршруты приложений
apps_router.include_router(router=auth_router)
apps_router.include_router(router=profile_router)
