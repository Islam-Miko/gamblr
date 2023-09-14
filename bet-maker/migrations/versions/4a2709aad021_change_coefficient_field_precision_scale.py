"""change coefficient field precision, scale

Revision ID: 4a2709aad021
Revises: fcffa4cda67d
Create Date: 2023-09-14 22:58:45.027212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a2709aad021'
down_revision: Union[str, None] = 'fcffa4cda67d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('event', 'coefficient', type_=sa.Numeric(5, 2))
    op.alter_column('bet', 'bid', type_=sa.Numeric(5, 2))


def downgrade() -> None:
    op.alter_column('event', 'coefficient', type_=sa.Numeric(2, 0))
    op.alter_column('bet', 'bid', type_=sa.Numeric(2, 0))
