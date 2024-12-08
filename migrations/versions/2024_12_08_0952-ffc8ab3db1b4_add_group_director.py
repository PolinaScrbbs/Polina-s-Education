"""add group director

Revision ID: ffc8ab3db1b4
Revises: e24189375df4
Create Date: 2024-12-08 09:52:29.488446

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ffc8ab3db1b4"
down_revision: Union[str, None] = "e24189375df4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("groups", sa.Column("director_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "groups", "users", ["director_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "groups", type_="foreignkey")
    op.drop_column("groups", "director_id")
    # ### end Alembic commands ###
