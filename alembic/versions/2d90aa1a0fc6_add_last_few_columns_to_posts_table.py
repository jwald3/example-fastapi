"""add last few columns to posts table

Revision ID: 2d90aa1a0fc6
Revises: 180ba6d07cb5
Create Date: 2022-02-03 13:39:19.523829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d90aa1a0fc6'
down_revision = '180ba6d07cb5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        "published", sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
