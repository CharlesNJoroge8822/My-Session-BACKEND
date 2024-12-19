"""final migration

Revision ID: 3854d80fbda9
Revises: 6e891169eaf4
Create Date: 2024-12-19 16:04:08.666131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3854d80fbda9'
down_revision: Union[str, None] = '6e891169eaf4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
