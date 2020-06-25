"""empty message

Revision ID: 237c69f3a2a6
Revises: 898f02ab1d2c
Create Date: 2020-06-25 05:24:31.295382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '237c69f3a2a6'
down_revision = '898f02ab1d2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
