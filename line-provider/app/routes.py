from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from .dependencies import check_event_exists
from .events import Event, EventState
from .redis import add_event
from .redis import get_events as get_active_events
from .redis import put_event, update_state

router = APIRouter(prefix="/events")

OKResponse = JSONResponse(content={"msg": "ok"})


@router.post("/", status_code=status.HTTP_200_OK)
async def create_event(event: Event):
    await add_event(event)
    return OKResponse


@router.get("/", response_model=list[Event])
async def get_events():
    # could add pagination
    return [Event(**event) async for event in get_active_events()]


@router.patch("/{event_id}/", status_code=status.HTTP_200_OK)
async def update_event_state(
    event_id: int = Depends(check_event_exists),
    new_state: EventState = Body(..., embed=True),
):
    await update_state(event_id, new_state)
    if new_state in (EventState.FINISHED_LOSE, EventState.FINISHED_WIN):
        await put_event(
            "finished_events", dict(event_id=event_id, state=new_state)
        )
    return OKResponse
