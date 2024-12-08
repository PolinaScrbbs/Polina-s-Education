"""add user group_id

Revision ID: dee95f49f27a
Revises: ffc8ab3db1b4
Create Date: 2024-12-08 10:01:47.653075

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dee95f49f27a"
down_revision: Union[str, None] = "ffc8ab3db1b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("group_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "users", "groups", ["group_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "group_id")
    # ### end Alembic commands ###
