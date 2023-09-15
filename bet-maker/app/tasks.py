import asyncio
from typing import Final

from loguru import logger
from pydantic import ValidationError

from .database import SessionFactory
from .redis import fetch_queue_data
from .services import EventService

NEW_EVENT_QUEUE: Final[str] = "new_events"
STATE_UPDATE_QUEUE: Final[str] = "finished_events"


async def listen_new_events() -> None:
    """
    Coroutine fetches new events from
    Redis queue.
    When events are fetched, they are stored in DB.
    """
    try:
        while True:
            new_events = await fetch_queue_data(NEW_EVENT_QUEUE)
            async with SessionFactory() as session:
                service = EventService.with_session(session)
                for event in new_events:
                    try:
                        await service.create_from_dict(event)
                    except ValidationError as e:
                        logger.error(e)
                        logger.error(event)
                        # TODO how to save event:
                        # save in queue again or in another table, database
                        continue
            await asyncio.sleep(10)
    except Exception as e:
        logger.error(e)


async def listen_state_update() -> None:
    """
    Coroutine fetches `state change` events from
    Redis queue.
    When events are fetched, their data are stored in DB.
    """
    try:
        while True:
            states = await fetch_queue_data(STATE_UPDATE_QUEUE)
            async with SessionFactory() as session:
                service = EventService.with_session(session)
                for state in states:
                    try:
                        await service.update_state_from_dict(state)
                    except ValidationError as e:
                        logger.error(e)
                        logger.error(state)
                        # TODO how to save state:
                        # save in queue again or in another table, database
                        continue
            await asyncio.sleep(5)
    except Exception as e:
        logger.error(e)
