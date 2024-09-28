"""modified some fields

Revision ID: b8941cb7aeb9
Revises: 76006084fbca
Create Date: 2024-09-28 15:10:54.804108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8941cb7aeb9'
down_revision: Union[str, None] = '76006084fbca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classrooms', sa.Column('name', sa.String(), nullable=False))
    op.add_column('classrooms', sa.Column('subject', sa.String(), nullable=False))
    op.add_column('classrooms', sa.Column('amount_of_students', sa.Integer(), nullable=False))
    op.drop_constraint('fk_students_id_users', 'students', type_='foreignkey')
    op.create_foreign_key(op.f('fk_students_id_users'), 'students', 'users', ['id'], ['id'], ondelete='cascade')
    op.alter_column('teachers', 'subject',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('teachers', 'subject',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(op.f('fk_students_id_users'), 'students', type_='foreignkey')
    op.create_foreign_key('fk_students_id_users', 'students', 'users', ['id'], ['id'])
    op.drop_column('classrooms', 'amount_of_students')
    op.drop_column('classrooms', 'subject')
    op.drop_column('classrooms', 'name')
    # ### end Alembic commands ###
