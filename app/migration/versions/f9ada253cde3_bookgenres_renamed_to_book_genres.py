"""bookgenres renamed to book_genres

Revision ID: f9ada253cde3
Revises: 3bd1b997a6c5
Create Date: 2025-01-29 10:57:15.944087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f9ada253cde3'
down_revision: Union[str, None] = '3bd1b997a6c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_genres',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.PrimaryKeyConstraint('book_id', 'genre_id')
    )
    op.drop_table('bookgenres')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookgenres',
    sa.Column('book_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='bookgenres_book_id_fkey'),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], name='bookgenres_genre_id_fkey'),
    sa.PrimaryKeyConstraint('book_id', 'genre_id', name='bookgenres_pkey')
    )
    op.drop_table('book_genres')
    # ### end Alembic commands ###
