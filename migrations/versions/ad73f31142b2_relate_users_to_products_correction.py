"""relate users to products-correction

Revision ID: ad73f31142b2
Revises: 89fd52dc68c6
Create Date: 2024-12-29 20:49:52.606793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ad73f31142b2'
down_revision: Union[str, None] = '89fd52dc68c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('user_uid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'products', 'users', ['user_uid'], ['uid'])
    op.drop_constraint('users_user_uid_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'user_uid')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_uid', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_user_uid_fkey', 'users', 'users', ['user_uid'], ['uid'])
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'user_uid')
    # ### end Alembic commands ###
