"""delete practice pattern

Revision ID: ddf4c59afa8a
Revises: 63bb285adba1
Create Date: 2024-12-08 12:33:00.857426

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ddf4c59afa8a"
down_revision: Union[str, None] = "63bb285adba1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint("practices_pattern_id_fkey", "practices", type_="foreignkey")

    # Drop the 'practice_patterns' table
    op.drop_table("practice_patterns")

    # Add the 'type' column to the 'practices' table
    op.add_column(
        "practices",
        sa.Column(
            "type",
            sa.Enum("EDUCATIONAL_PRACTICE", "PRODUCTION_PRACTICE", name="practicetype"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "practices",
        sa.Column("pattern_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "practices_pattern_id_fkey",
        "practices",
        "practice_patterns",
        ["pattern_id"],
        ["id"],
    )
    op.drop_column("practices", "type")
    op.create_table(
        "practice_patterns",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM(
                "EDUCATIONAL_PRACTICE", "PRODUCTION_PRACTICE", name="practicetype"
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "specialization_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("course_number", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["specialization_id"],
            ["specializations.id"],
            name="practice_patterns_specialization_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id", name="practice_patterns_pkey"),
    )
    # ### end Alembic commands ###
