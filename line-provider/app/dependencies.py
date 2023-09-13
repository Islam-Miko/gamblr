from fastapi import HTTPException, status

from .redis import exists_key


async def check_event_exists(event_id: int) -> int:
    if not await exists_key(event_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No event with given id!",
        )
    return event_id
