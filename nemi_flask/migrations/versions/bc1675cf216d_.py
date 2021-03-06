"""empty message

Revision ID: bc1675cf216d
Revises: 67345ab04a1e
Create Date: 2018-04-03 23:32:38.012738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc1675cf216d'
down_revision = '67345ab04a1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nemi_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_from_id', sa.Integer(), nullable=True),
    sa.Column('user_to_id', sa.Integer(), nullable=True),
    sa.Column('contant', sa.String(length=100), nullable=True),
    sa.Column('checked', sa.Boolean(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_from_id'], ['nemi_user.id'], ),
    sa.ForeignKeyConstraint(['user_to_id'], ['nemi_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nemi_message')
    # ### end Alembic commands ###
