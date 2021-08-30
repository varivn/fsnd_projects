"""empty message

Revision ID: cace952ca4e7
Revises: 
Create Date: 2021-08-27 20:35:14.663599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cace952ca4e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('artist', sa.Column('looking4', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('looking4', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'looking4')
    op.drop_column('venue', 'website_link')
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'looking4')
    op.drop_column('artist', 'website_link')
    # ### end Alembic commands ###