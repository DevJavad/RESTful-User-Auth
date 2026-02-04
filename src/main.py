import uvicorn
from router import router
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

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)