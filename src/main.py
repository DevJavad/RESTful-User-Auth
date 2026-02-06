import uvicorn
from router import user_router
from fastapi import FastAPI
from core.config import settings
from db import connect, disconnect
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect(settings.DATABASE_URL)
    yield
    await disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)