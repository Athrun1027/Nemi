"""empty message

Revision ID: cdcd3b3d6a62
Revises: bc1675cf216d
Create Date: 2018-04-07 16:21:28.794839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdcd3b3d6a62'
down_revision = 'bc1675cf216d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nemi_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('is_enable', sa.Boolean(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('nickname', sa.String(length=60), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.Column('edit_time', sa.DateTime(), nullable=True),
    sa.Column('disable_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['nemi_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('nemi_user_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['nemi_group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['nemi_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('nemi_space', sa.Column('own_group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'nemi_space', 'nemi_group', ['own_group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'nemi_space', type_='foreignkey')
    op.drop_column('nemi_space', 'own_group_id')
    op.drop_table('nemi_user_group')
    op.drop_table('nemi_group')
    # ### end Alembic commands ###