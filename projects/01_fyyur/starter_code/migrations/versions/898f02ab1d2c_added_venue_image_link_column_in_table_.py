"""Added venue image link column in table shows.

Revision ID: 898f02ab1d2c
Revises: 74e628ef8f0a
Create Date: 2020-06-25 04:44:27.194472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '898f02ab1d2c'
down_revision = '74e628ef8f0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'venue_image_link')
    # ### end Alembic commands ###