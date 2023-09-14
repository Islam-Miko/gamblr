"""create tables

Revision ID: fcffa4cda67d
Revises: 
Create Date: 2023-09-14 15:39:08.841113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcffa4cda67d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "event",
        sa.Column("event_id", sa.BigInteger, primary_key=True, autoincrement=False),
        sa.Column("coefficient", sa.Numeric(precision=2, asdecimal=True), nullable=False),
        sa.Column("deadline", sa.BigInteger, nullable=False),
        sa.Column("state", sa.SmallInteger, nullable=False)
    )
    op.create_table(
        "bet",
        sa.Column("bet_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("event_id", sa.BigInteger, sa.ForeignKey("event.event_id"),),
        sa.Column("bid", sa.Numeric(precision=2, asdecimal=True), nullable=False)
    )
    op.create_index("bet_event_id_idx", "bet", ["event_id"], unique=False)


def downgrade() -> None:
    op.drop_table("bet")
    op.drop_table("event")
