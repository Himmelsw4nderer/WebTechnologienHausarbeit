"""empty message

Revision ID: 52e129d00b28
Revises: 
Create Date: 2024-05-12 09:30:07.063973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52e129d00b28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('public', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players_games',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('game_id', 'player_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players_games')
    op.drop_table('game')
    op.drop_table('player')
    # ### end Alembic commands ###