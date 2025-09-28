import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"status": "It's ALIVE!"}


def start():
    uvicorn.run(app="fat.main:app", reload=True)
