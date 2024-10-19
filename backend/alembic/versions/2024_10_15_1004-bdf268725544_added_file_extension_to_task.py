"""added file_extension to task

Revision ID: bdf268725544
Revises: cc1d026d13a1
Create Date: 2024-10-15 10:04:02.850158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdf268725544'
down_revision: Union[str, None] = 'cc1d026d13a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('file_extension', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'file_extension')
    # ### end Alembic commands ###
