"""performance added

Revision ID: e7561ece5d14
Revises: 4d0bb6b4dbcc
Create Date: 2024-09-17 23:03:56.513471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7561ece5d14'
down_revision: Union[str, None] = '4d0bb6b4dbcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classrooms_performance',
    sa.Column('classroom_id', sa.Uuid(), nullable=False),
    sa.Column('task_type', sa.Integer(), nullable=False),
    sa.Column('total_solved', sa.Integer(), nullable=False),
    sa.Column('correct_solved', sa.Integer(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], name=op.f('fk_classrooms_performance_classroom_id_classrooms')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_classrooms_performance')),
    sa.UniqueConstraint('classroom_id', 'task_type', name='idx_unique_classroom_task_type')
    )
    op.create_table('students_performance',
    sa.Column('student_id', sa.Uuid(), nullable=False),
    sa.Column('classroom_id', sa.Uuid(), nullable=False),
    sa.Column('task_type', sa.Integer(), nullable=False),
    sa.Column('total_solved', sa.Integer(), nullable=False),
    sa.Column('correct_solved', sa.Integer(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], name=op.f('fk_students_performance_classroom_id_classrooms')),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name=op.f('fk_students_performance_student_id_students')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_students_performance')),
    sa.UniqueConstraint('student_id', 'classroom_id', 'task_type', name='idx_unique_student_classroom_task_type')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students_performance')
    op.drop_table('classrooms_performance')
    # ### end Alembic commands ###
