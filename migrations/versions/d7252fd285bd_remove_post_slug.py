"""Remove post slug

Revision ID: d7252fd285bd
Revises: 4c31ffedf980
Create Date: 2020-11-25 22:30:01.488773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd7252fd285bd'
down_revision = '4c31ffedf980'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('slug', table_name='post')
    op.drop_column('post', 'slug')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('slug', mysql.VARCHAR(length=128), nullable=True))
    op.create_index('slug', 'post', ['slug'], unique=True)
    # ### end Alembic commands ###
