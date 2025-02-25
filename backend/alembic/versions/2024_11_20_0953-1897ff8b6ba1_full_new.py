"""full new

Revision ID: 1897ff8b6ba1
Revises: bdf268725544
Create Date: 2024-11-20 09:53:03.847977

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1897ff8b6ba1"
down_revision: Union[str, None] = "bdf268725544"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('students')
    # op.drop_table('teachers')
    op.add_column(
        "classrooms",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "classrooms",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.drop_constraint(
        "fk_classrooms_teacher_id_teachers", "classrooms", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_classrooms_teacher_id_users"),
        "classrooms",
        "users",
        ["teacher_id"],
        ["id"],
        ondelete="cascade",
    )
    op.drop_constraint(
        "fk_student_classroom_associations_student_id_students",
        "student_classroom_associations",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_student_classroom_associations_student_id_users"),
        "student_classroom_associations",
        "users",
        ["student_id"],
        ["id"],
    )
    op.drop_constraint(
        "fk_student_variant_associations_student_id_students",
        "student_variant_associations",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_student_variant_associations_student_id_users"),
        "student_variant_associations",
        "users",
        ["student_id"],
        ["id"],
    )
    op.drop_constraint(
        "fk_students_performance_student_id_students",
        "students_performance",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_students_performance_student_id_users"),
        "students_performance",
        "users",
        ["student_id"],
        ["id"],
    )
    op.add_column(
        "tasks",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.add_column(
        "tasks",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
    )
    op.drop_constraint("fk_tasks_teacher_id_teachers", "tasks", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_tasks_teacher_id_users"),
        "tasks",
        "users",
        ["teacher_id"],
        ["id"],
        ondelete="cascade",
    )
    op.add_column(
        "users",
        sa.Column(
            "subject",
            sa.Enum(
                "informatics",
                "math",
                "russian",
                "english",
                "french",
                "spanish",
                "german",
                "history",
                "social_studies",
                "geography",
                "biology",
                "chemistry",
                "physics",
                native_enum=False,
            ),
            nullable=True,
        ),
    )
    op.drop_constraint(
        "fk_variants_teacher_id_teachers", "variants", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_variants_teacher_id_users"),
        "variants",
        "users",
        ["teacher_id"],
        ["id"],
        ondelete="cascade",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_variants_teacher_id_users"), "variants", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_variants_teacher_id_teachers",
        "variants",
        "teachers",
        ["teacher_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("users", "subject")
    op.drop_constraint(op.f("fk_tasks_teacher_id_users"), "tasks", type_="foreignkey")
    op.create_foreign_key(
        "fk_tasks_teacher_id_teachers",
        "tasks",
        "teachers",
        ["teacher_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("tasks", "updated_at")
    op.drop_column("tasks", "created_at")
    op.drop_constraint(
        op.f("fk_students_performance_student_id_users"),
        "students_performance",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_students_performance_student_id_students",
        "students_performance",
        "students",
        ["student_id"],
        ["id"],
    )
    op.drop_constraint(
        op.f("fk_student_variant_associations_student_id_users"),
        "student_variant_associations",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_student_variant_associations_student_id_students",
        "student_variant_associations",
        "students",
        ["student_id"],
        ["id"],
    )
    op.drop_constraint(
        op.f("fk_student_classroom_associations_student_id_users"),
        "student_classroom_associations",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_student_classroom_associations_student_id_students",
        "student_classroom_associations",
        "students",
        ["student_id"],
        ["id"],
    )
    op.drop_constraint(
        op.f("fk_classrooms_teacher_id_users"), "classrooms", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_classrooms_teacher_id_teachers",
        "classrooms",
        "teachers",
        ["teacher_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("classrooms", "updated_at")
    op.drop_column("classrooms", "created_at")
    op.create_table(
        "teachers",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("subject", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["id"], ["users.id"], name="fk_teachers_id_users"),
        sa.PrimaryKeyConstraint("id", name="pk_teachers"),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["users.id"], name="fk_students_id_users", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_students"),
    )
    # ### end Alembic commands ###
