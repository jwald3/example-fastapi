"""add foreign key to posts table

Revision ID: 180ba6d07cb5
Revises: 899623622dba
Create Date: 2022-02-03 13:25:26.849538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '180ba6d07cb5'
down_revision = '899623622dba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',     # unique key name
    source_table="posts",       # current table 
    referent_table="users",     # table to be linked to
    local_cols=["owner_id"],    # column to establish relationship in current table
    remote_cols=['id'],         # column to connect to from linked table
    ondelete="CASCADE"          # cascade changes
    )


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')

