"""empty message

Revision ID: 7fe95005cad1
Revises: 6b62a1bcd456
Create Date: 2024-05-14 08:55:35.401285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fe95005cad1'
down_revision = '6b62a1bcd456'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('settings_starting_card_amount', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('settings_black_card_finish', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('settings_black_on_black', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('settings_plus_two_stacking', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('settings_plus_two_stacking')
        batch_op.drop_column('settings_black_on_black')
        batch_op.drop_column('settings_black_card_finish')
        batch_op.drop_column('settings_starting_card_amount')

    # ### end Alembic commands ###