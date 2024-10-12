"""added file_id to tasks

Revision ID: 82d010683013
Revises: d5a7da73ec7a
Create Date: 2024-10-12 17:24:04.348199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82d010683013'
down_revision: Union[str, None] = 'd5a7da73ec7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('file_id', sa.Uuid(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'file_id')
    # ### end Alembic commands ###
