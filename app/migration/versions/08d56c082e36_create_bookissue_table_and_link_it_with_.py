"""create bookissue table and link it with user and book tables

Revision ID: 08d56c082e36
Revises: 6bc24a1e13a2
Create Date: 2025-01-30 17:35:20.272265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08d56c082e36'
down_revision: Union[str, None] = '6bc24a1e13a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
