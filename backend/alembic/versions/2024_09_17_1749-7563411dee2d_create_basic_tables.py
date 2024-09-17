"""create basic tables

Revision ID: 7563411dee2d
Revises: 
Create Date: 2024-09-17 17:49:59.156731

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7563411dee2d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.LargeBinary(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column(
            "role_type", sa.Enum("TEACHER", "STUDENT", name="roletype"), nullable=False
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["users.id"], name=op.f("fk_students_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_students")),
    )
    op.create_table(
        "teachers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("subject", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["users.id"], name=op.f("fk_teachers_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teachers")),
    )
    op.create_table(
        "tasks",
        sa.Column("type", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), server_default="", nullable=False),
        sa.Column(
            "type_of_answer",
            sa.Enum("FULL_ANSWER", "SHORT_ANSWER", name="answertype"),
            nullable=False,
        ),
        sa.Column("teacher_id", sa.Uuid(), nullable=False),
        sa.Column("correct_answer", sa.String(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["teachers.id"],
            name=op.f("fk_tasks_teacher_id_teachers"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )
    op.create_table(
        "variants",
        sa.Column("teacher_id", sa.Uuid(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["teachers.id"],
            name=op.f("fk_variants_teacher_id_teachers"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_variants")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("variants")
    op.drop_table("tasks")
    op.drop_table("teachers")
    op.drop_table("students")
    op.drop_table("users")
    # ### end Alembic commands ###
