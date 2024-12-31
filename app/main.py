from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.endpoints import image
from app.database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(image.router, prefix="/api/v1")
