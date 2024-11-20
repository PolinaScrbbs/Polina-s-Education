"""interger course_number

Revision ID: 55e3c0a41bb6
Revises: 8261524d6882
Create Date: 2024-11-20 10:44:32.612673

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "55e3c0a41bb6"
down_revision: Union[str, None] = "8261524d6882"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Преобразование столбца evaluation в INTEGER
    op.execute(
        """
        ALTER TABLE lesson_result_evaluations 
        ALTER COLUMN evaluation TYPE INTEGER USING evaluation::INTEGER
    """
    )

    # Преобразование столбца course_number в INTEGER
    op.execute(
        """
        ALTER TABLE practice_patterns 
        ALTER COLUMN course_number TYPE INTEGER USING course_number::INTEGER
    """
    )


def downgrade() -> None:
    # Обратное преобразование столбца evaluation в CHAR(1)
    op.execute(
        """
        ALTER TABLE lesson_result_evaluations 
        ALTER COLUMN evaluation TYPE CHAR(1) USING evaluation::CHAR
    """
    )

    # Обратное преобразование столбца course_number в CHAR(1)
    op.execute(
        """
        ALTER TABLE practice_patterns 
        ALTER COLUMN course_number TYPE CHAR(1) USING course_number::CHAR
    """
    )
