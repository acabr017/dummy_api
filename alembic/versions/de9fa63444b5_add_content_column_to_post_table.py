"""add content column to post table

Revision ID: de9fa63444b5
Revises: 61bb6e086f50
Create Date: 2022-07-09 12:44:48.974148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de9fa63444b5'
down_revision = '61bb6e086f50'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
