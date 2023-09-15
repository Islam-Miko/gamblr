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
        for task in self.__tasks:
            task.cancel("Gracefully canceled!")
        await asyncio.sleep(3)
        logger.info("Gracefully canceled coros")


event_listener = EventListener(listen_new_events, listen_state_update)
