import decimal

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class EventUpdateSchema(BaseSchema):
    event_id: int
    state: int


class EventSchema(EventUpdateSchema):
    coefficient: decimal.Decimal
    deadline: int


class BetSchema(BaseSchema):
    bet_id: int
    state: int


class BetCreateSchema(BaseSchema):
    event_id: int
    bid: decimal.Decimal = Field(..., gt=0, decimal_places=2, le=1000)


class PaginationResponse(BaseSchema):
    count: int
    limit: int
    data: list
    offset: int


class EventPaginationResponse(PaginationResponse):
    data: list[EventSchema]


class BetPaginationResponse(PaginationResponse):
    data: list[BetSchema]
