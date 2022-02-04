"""create posts table

Revision ID: ddcdb246f9d8
Revises: 
Create Date: 2022-02-03 12:19:11.676981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddcdb246f9d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    'title', sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
