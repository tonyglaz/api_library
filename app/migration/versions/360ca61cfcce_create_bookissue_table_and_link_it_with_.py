"""create bookissue table and link it with user and book table3

Revision ID: 360ca61cfcce
Revises: ed3d6aa44ceb
Create Date: 2025-01-30 18:17:50.853640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '360ca61cfcce'
down_revision: Union[str, None] = 'ed3d6aa44ceb'
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
