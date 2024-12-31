"""non-nullable first last name in  users table

Revision ID: 780b6d86c2d3
Revises: 949d5c704d57
Create Date: 2024-12-29 12:56:04.566598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '780b6d86c2d3'
down_revision: Union[str, None] = '949d5c704d57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
