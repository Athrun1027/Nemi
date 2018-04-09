"""empty message

Revision ID: 67345ab04a1e
Revises: 51b34097dea5
Create Date: 2018-04-03 18:24:39.500695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67345ab04a1e'
down_revision = '51b34097dea5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('nemi_user', sa.Column('college_in', sa.String(length=60), nullable=True))
    op.add_column('nemi_user', sa.Column('img_url', sa.String(length=200), nullable=True))
    op.add_column('nemi_user', sa.Column('nick_call', sa.String(length=60), nullable=True))
    op.add_column('nemi_user', sa.Column('school_in', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('nemi_user', 'school_in')
    op.drop_column('nemi_user', 'nick_call')
    op.drop_column('nemi_user', 'img_url')
    op.drop_column('nemi_user', 'college_in')
    # ### end Alembic commands ###