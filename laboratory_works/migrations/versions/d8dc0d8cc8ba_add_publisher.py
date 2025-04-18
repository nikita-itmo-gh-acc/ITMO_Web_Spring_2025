"""add publisher

Revision ID: d8dc0d8cc8ba
Revises: 0ad6b4876544
Create Date: 2025-04-12 16:44:18.128637

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8dc0d8cc8ba'
down_revision: Union[str, None] = '0ad6b4876544'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookinfo', sa.Column('publisher', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookinfo', 'publisher')
    # ### end Alembic commands ###
