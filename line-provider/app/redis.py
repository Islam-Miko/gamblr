import json
from collections.abc import AsyncIterator, Mapping
from typing import Any

from redis.asyncio import Redis

from .events import Event, EventState

redis_client: Redis = None


async def set_event(event: Event) -> None:
    await redis_client.hmset(event.event_id, event.model_dump())


async def add_event(event: Event) -> None:
    data = event.model_dump()
    async with redis_client.pipeline() as pipe:
        await pipe.hmset(event.event_id, data)
        await pipe.lpush("new_events", json.dumps(data))
        await pipe.execute()


async def get_events() -> AsyncIterator[dict]:
    cur = "0"
    while cur:
        cur, keys = await redis_client.scan(int(cur), _type="HASH")
        for key in keys:
            event = await redis_client.hgetall(key)
            yield event


async def update_state(event_id: int, state: EventState) -> None:
    await redis_client.hset(event_id, "state", state.value)


async def put_event(queue_name: str, data: Mapping) -> None:
    data_str = json.dumps(data)
    await redis_client.lpush(queue_name, data_str)


async def exists_key(key: Any) -> bool:
    return int(await redis_client.exists(key)) == 1
