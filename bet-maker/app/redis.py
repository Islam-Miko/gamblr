import json

from loguru import logger
from redis.asyncio import Redis

redis_client: Redis = None


async def fetch_queue_data(queue_name: str) -> list[dict] | list:
    data_count = await redis_client.llen(queue_name)
    if data_count == 0:
        logger.info("Queue: {queue} is empty!", queue=queue_name)
        return []
    data = await redis_client.rpop(queue_name, data_count)
    return [json.loads(item) for item in data]
