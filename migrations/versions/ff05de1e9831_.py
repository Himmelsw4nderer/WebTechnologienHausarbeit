"""empty message

Revision ID: ff05de1e9831
Revises: 106ddfc4c232
Create Date: 2024-05-21 20:28:22.892066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff05de1e9831'
down_revision = '106ddfc4c232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_card_color_selection', sa.String(length=20), nullable=True))

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('has_finished', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('last_place', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('sayed_uno', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_column('sayed_uno')
        batch_op.drop_column('last_place')
        batch_op.drop_column('has_finished')

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('last_card_color_selection')

    # ### end Alembic commands ###