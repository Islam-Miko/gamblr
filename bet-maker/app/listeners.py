import asyncio
from asyncio import Task
from collections.abc import Awaitable, Callable

from loguru import logger

from .tasks import listen_new_events, listen_state_update

AsyncListenerFunc = Callable[[], Awaitable[None]]


class EventListener:
    def __init__(self, *funcs: list[AsyncListenerFunc]) -> None:
        self.__funcs = funcs
        self.__tasks: list[Task]

    async def start_listening(self) -> None:
        logger.info("Staring listener tasks")
        self.__tasks = [asyncio.create_task(coro()) for coro in self.__funcs]
        logger.info("Started tasks")

    async def stop_listening(self) -> None:
        logger.info("Canceling listener tasks")
        cancel_tasks = [task.cancel() for task in self.__tasks]
        await asyncio.gather(cancel_tasks)
        logger.info("Gracefully canceled coros")


event_listener = EventListener(listen_new_events, listen_state_update)
