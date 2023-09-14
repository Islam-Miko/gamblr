import json
from typing import Final

from loguru import logger
from redis.asyncio import Redis

redis_client: Redis = None

NEW_EVENT_QUEUE: Final[str] = "new_events"
STATE_UPDATE_QUEUE: Final[str] = "finished_events"


async def fetch_new_events() -> list[dict] | list:
    new_events_count = await redis_client.llen(NEW_EVENT_QUEUE)
    if new_events_count == 0:
        logger.info("No new events")
        return []
    events = await redis_client.rpop(NEW_EVENT_QUEUE, new_events_count)

    if isinstance(events, list):
        return [json.loads(event) for event in events]
    return [json.loads(events)]


async def fetch_states() -> list[dict] | list:
    states_count = await redis_client.llen(STATE_UPDATE_QUEUE)
    if states_count == 0:
        logger.info("No state updates")
        return []
    states = await redis_client.rpop(STATE_UPDATE_QUEUE, states_count)
    if isinstance(states, list):
        return [json.loads(state) for state in states]
    return [json.loads(states)]
