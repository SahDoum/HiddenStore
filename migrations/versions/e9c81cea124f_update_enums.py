"""UPDATE ENUMS

Revision ID: e9c81cea124f
Revises: e396090eb822
Create Date: 2024-08-22 11:39:29.058429

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9c81cea124f"
down_revision: Union[str, None] = "e396090eb822"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Create the paymentstatus
    # Define the existing paymentstatus enum
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'CREATED'")
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'PENDING'")
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'CONFIRMED'")
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'FAILED'")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
