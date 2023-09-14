import decimal

from sqlalchemy import BigInteger, ForeignKey, Numeric, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "event"

    event_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=False
    )
    coefficient: Mapped[decimal.Decimal] = mapped_column(
        Numeric(precision=2, asdecimal=True),
    )
    deadline: Mapped[int] = mapped_column(BigInteger)
    state: Mapped[int] = mapped_column(SmallInteger)


class Bet(Base):
    __tablename__ = "bet"

    bet_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    event_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("event.event_id"), index=True
    )
    bid: Mapped[decimal.Decimal] = mapped_column(
        Numeric(precision=2, asdecimal=True)
    )
