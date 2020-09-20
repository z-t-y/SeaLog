"""empty message

Revision ID: 780c29109b25
Revises: 911cc5d772fc
Create Date: 2020-08-30 15:22:15.026266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '780c29109b25'
down_revision = '911cc5d772fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'feedback', 'user', ['author_id'], ['id'])
    op.drop_column('feedback', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feedback', sa.Column('author', sa.VARCHAR(length=20), nullable=True))
    op.drop_constraint(None, 'feedback', type_='foreignkey')
    # ### end Alembic commands ###