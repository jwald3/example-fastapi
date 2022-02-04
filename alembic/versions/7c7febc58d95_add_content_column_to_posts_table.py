"""add content column to posts table

Revision ID: 7c7febc58d95
Revises: ddcdb246f9d8
Create Date: 2022-02-03 12:46:22.121635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c7febc58d95'
down_revision = 'ddcdb246f9d8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
