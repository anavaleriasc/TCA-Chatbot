"""alteracao de chave estrangeira

Revision ID: 02e8170187ad
Revises: f8bb92070270
Create Date: 2026-06-05 11:55:20.236632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02e8170187ad'
down_revision: Union[str, Sequence[str], None] = 'f8bb92070270'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
