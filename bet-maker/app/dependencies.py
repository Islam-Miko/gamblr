from fastapi import Depends, HTTPException, status

from .repositories import BetRepository, get_bet_repository
from .schemas import BetsCreateSchema


async def check_bet_exists(
    bet: BetsCreateSchema,
    repository: BetRepository = Depends(get_bet_repository),
) -> BetsCreateSchema:
    if not await repository.exists_id(bet.bet_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No bet with given id!",
        )
    return bet
