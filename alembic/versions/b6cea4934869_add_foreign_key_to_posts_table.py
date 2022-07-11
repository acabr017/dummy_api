"""add foreign key to posts table

Revision ID: b6cea4934869
Revises: 95a5cf98c026
Create Date: 2022-07-09 12:57:54.835205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6cea4934869'
down_revision = '95a5cf98c026'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_FK', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_FK', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
