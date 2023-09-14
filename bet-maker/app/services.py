from collections.abc import Mapping
from typing import Generic, TypeVar

from fastapi import Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import (
    BetRepository,
    EventRepository,
    get_bet_repository,
    get_event_repository,
)
from .schemas import (
    BaseSchema,
    BetCreateSchema,
    BetSchema,
    EventSchema,
    EventUpdateSchema,
)

Schema = TypeVar("Schema", bound=BaseSchema)


class BaseService(Generic[Schema]):
    schema: Schema

    async def list(self, limit: int = 20, offset: int = 0):
        data, count_stmt = await self.repository.list(limit, offset)
        count = await self.repository.count(count_stmt)
        return {
            "count": count,
            "limit": limit,
            "offset": offset,
            "data": [item for item in data],
        }

    async def create(self, event: Schema) -> int:
        id_ = await self.repository.create(event.model_dump())
        await self.repository.commit()
        return id_


class EventService(BaseService[EventSchema]):
    schema = EventSchema

    def __init__(
        self, repo: EventRepository = Depends(get_event_repository)
    ) -> None:
        self.repository = repo

    @classmethod
    def with_session(cls, session: AsyncSession):
        return cls(get_event_repository(session))

    async def update_state(self, event: EventUpdateSchema) -> None:
        try:
            await self.repository.update(
                event.event_id, event.model_dump(include={"state"})
            )
        except Exception:
            pass
        else:
            await self.repository.commit()

    async def create_from_dict(self, data: Mapping) -> int:
        try:
            event = self.schema.model_validate(data)
        except ValidationError as e:
            raise e
        else:
            return await self.create(event)

    async def update_state_from_dict(self, data: Mapping) -> None:
        event = EventUpdateSchema.model_validate(data)
        await self.update_state(event)


class BetService(BaseService[BetSchema]):
    schema = BetSchema

    def __init__(
        self, repo: BetRepository = Depends(get_bet_repository)
    ) -> None:
        self.repository = repo

    @classmethod
    def with_session(cls, session: AsyncSession):
        return cls(get_bet_repository(session))

    async def create(self, bet: BetCreateSchema) -> int:
        id_ = await self.repository.create(bet.model_dump())
        await self.repository.commit()
        return id_
