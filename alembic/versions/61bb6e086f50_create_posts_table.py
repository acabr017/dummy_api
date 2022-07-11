"""create posts table

Revision ID: 61bb6e086f50
Revises: 
Create Date: 2022-07-09 12:34:48.433474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61bb6e086f50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
