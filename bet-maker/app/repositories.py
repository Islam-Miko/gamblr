from collections.abc import Mapping
from datetime import datetime
from typing import Generic, Type, TypeVar

from fastapi import Depends
from sqlalchemy import Select
from sqlalchemy import exists as sql_exists
from sqlalchemy import func, insert, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .models import Base, Bet, Event

Model = TypeVar("Model", bound=Base)
Key = TypeVar("Key", int, str)


class BaseRepository(Generic[Model]):
    select_stmt: Select
    model: Type[Model]

    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def list(
        self,
        offset: int,
        limit: int,
    ):
        stmt = self.select_stmt
        result: Result = await self.session.execute(
            self.select_stmt.limit(limit).offset(offset)
        )
        return result.scalars().all(), stmt

    async def count(self, stmt: Select) -> int:
        stmt = select(func.count()).select_from(stmt.limit(None).offset(None))
        result: Result = await self.session.execute(stmt)
        return result.scalar_one()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


class EventRepository(BaseRepository[Event]):
    select_stmt: Select = select(
        Event.event_id,
        Event.state,
        Event.coefficient,
        Event.deadline,
    )

    async def create(self, data: Mapping) -> int:
        stmt = insert(self.model).values(data).returning(self.model.event_id)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, id: Key, data: Mapping) -> None:
        stmt = (
            update(self.model).where(self.model.event_id == id).values(**data)
        )
        await self.session.execute(stmt)

    async def list(self, limit: int, offset: int):
        stmt = self.select_stmt.where(
            self.model.deadline > int(datetime.now().timestamp())
        )
        result: Result = await self.session.execute(
            stmt.limit(limit).offset(offset)
        )
        return result.scalars().all(), stmt


class BetRepository(BaseRepository[Bet]):
    select_stmt: Select = (
        select(Bet.bet_id, Event.state)
        .select_from(Bet)
        .join(Event, onclause=Event.event_id == Bet.event_id)
    )

    async def create(self, data: Mapping) -> int:
        stmt = insert(self.model).values(data).returning(self.model.bet_id)
        result: Result = await self.session.execute(stmt)
        return result.scalar_one()

    async def update(self, id: Key, data: Mapping) -> None:
        stmt = update(self.model).where(self.model.bet_id == id).values(**data)
        await self.session.execute(stmt)

    async def exists_id(self, id: Key) -> bool:
        stmt = sql_exists(Bet).where(Bet.bet_id == id).select()
        result: Result = await self.session.execute(stmt)
        return result.scalar_one()


def get_event_repository(
    session: AsyncSession = Depends(get_session),
) -> EventRepository:
    return EventRepository(Event, session)


def get_bet_repository(
    session: AsyncSession = Depends(get_session),
) -> BetRepository:
    return BetRepository(Bet, session)
