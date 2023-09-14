import decimal
import enum

from pydantic import BaseModel, Field, field_serializer


class EventState(enum.IntEnum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    event_id: int
    coefficient: decimal.Decimal = Field(..., ge=0, decimal_places=2, le=1000)
    deadline: int
    state: EventState

    @field_serializer("coefficient")
    def serializer_coefficient(self, coefficient: decimal.Decimal) -> str:
        return str(coefficient)

    @field_serializer("state")
    def serializer_state(self, state: EventState) -> int:
        return state.value
