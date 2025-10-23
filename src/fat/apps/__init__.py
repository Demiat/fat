from fastapi import APIRouter

from fat.apps.auth.routes import auth_router

apps_router = APIRouter(prefix="/api/v1")

# Подключаем маршруты приложения auth
apps_router.include_router(router=auth_router)
