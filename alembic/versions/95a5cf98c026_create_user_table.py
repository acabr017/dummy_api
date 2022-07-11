"""create user table

Revision ID: 95a5cf98c026
Revises: de9fa63444b5
Create Date: 2022-07-09 12:49:08.269535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95a5cf98c026'
down_revision = 'de9fa63444b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
