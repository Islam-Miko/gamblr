from fastapi import APIRouter, Depends, status

from .dependencies import check_bet_exists
from .schemas import BetsCreateSchema
from .services import BetService, EventService

router = APIRouter()


@router.get("/events")
async def get_active_events(
    limit: int = 20, offset: int = 0, service: EventService = Depends()
):
    return await service.list(limit, offset)


@router.get("/bets")
async def get_bets(
    limit: int = 20, offset: int = 0, service: BetService = Depends()
):
    return await service.list(limit, offset)


@router.post("/bet", status_code=status.HTTP_201_CREATED)
async def make_bet(
    bet: BetsCreateSchema = Depends(check_bet_exists),
    service: BetService = Depends(),
):
    id_ = await service.create(bet)
    return {"bet_id": id_}
