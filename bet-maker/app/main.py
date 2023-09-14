from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI

from . import redis
from .routes import router
from .settings import get_settings

SETTINGS = get_settings()


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator:
    pool = aioredis.ConnectionPool.from_url(
        SETTINGS.REDIS_DSN, max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    yield
    await pool.disconnect()


app = FastAPI(title="Bet-maker", lifespan=lifespan)


@app.get("/health")
async def check_health():
    return {"ok": True}


app.include_router(router)
