from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
import redis.asyncio as aioredis
from . import redis
from .settings import get_settings
from .routes import router




settings = get_settings()


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator:
    pool = aioredis.ConnectionPool.from_url(
        settings.REDIS_DSN, max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    yield
    await pool.disconnect()

app = FastAPI(
    title="Line-provider", lifespan=lifespan
)

app.include_router(router)