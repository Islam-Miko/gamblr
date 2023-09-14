from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings import get_settings

SETTINGS = get_settings()

db_engine = create_async_engine(
    SETTINGS.POSTGRES_DSN,
)

SessionFactory = sessionmaker(
    db_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as s:
        yield s
