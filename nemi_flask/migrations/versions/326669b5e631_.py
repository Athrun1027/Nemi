"""empty message

Revision ID: 326669b5e631
Revises: 5a78b473b549
Create Date: 2018-04-08 23:13:22.753103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '326669b5e631'
down_revision = '5a78b473b549'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('nemi_share_file_ibfk_2', 'nemi_share_file', type_='foreignkey')
    op.create_foreign_key(None, 'nemi_share_file', 'nemi_file', ['original_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'nemi_share_file', type_='foreignkey')
    op.create_foreign_key('nemi_share_file_ibfk_2', 'nemi_share_file', 'nemi_user', ['original_id'], ['id'])
    # ### end Alembic commands ###
