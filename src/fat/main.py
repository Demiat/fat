import uvicorn
from fastapi import FastAPI

from .core.settings import settings
from fat.apps import apps_router

app = FastAPI()

app.include_router(router=apps_router)


def start():
    uvicorn.run(app="fat.main:app", reload=True)


@app.get("/")
async def index():
    return {"settings": settings.db_settings.db_url}
