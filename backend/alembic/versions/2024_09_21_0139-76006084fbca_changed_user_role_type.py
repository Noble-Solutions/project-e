"""changed user role type

Revision ID: 76006084fbca
Revises: e7561ece5d14
Create Date: 2024-09-21 01:39:47.681164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '76006084fbca'
down_revision: Union[str, None] = 'e7561ece5d14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('teachers', 'subject',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'role_type',
               existing_type=postgresql.ENUM('TEACHER', 'STUDENT', name='roletype'),
               type_=sa.Enum('teacher', 'student', native_enum=False),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_type',
               existing_type=sa.Enum('teacher', 'student', native_enum=False),
               type_=postgresql.ENUM('TEACHER', 'STUDENT', name='roletype'),
               existing_nullable=False)
    op.alter_column('teachers', 'subject',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
