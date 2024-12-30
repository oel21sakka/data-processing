from fastapi import FastAPI
from app.api.v1.endpoints import image

app = FastAPI()

app.include_router(image.router, prefix="/api/v1")
