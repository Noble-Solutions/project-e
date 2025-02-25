"""added subject  for variant

Revision ID: 74b2d4b0c2f6
Revises: c9505ba4b89d
Create Date: 2025-02-01 21:09:10.453651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74b2d4b0c2f6'
down_revision: Union[str, None] = 'c9505ba4b89d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('variants', sa.Column('subject', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('variants', 'subject')
    # ### end Alembic commands ###
