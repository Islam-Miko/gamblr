from fastapi import Depends, HTTPException, status

from .repositories import EventRepository, get_event_repository
from .schemas import BetCreateSchema


async def check_event_exists(
    bet: BetCreateSchema,
    repository: EventRepository = Depends(get_event_repository),
) -> BetCreateSchema:
    if not await repository.exists_id(bet.event_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No event with given id!",
        )
    return bet
