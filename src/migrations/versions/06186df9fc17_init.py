"""init

Revision ID: 06186df9fc17
Revises: 
Create Date: 2020-07-09 15:45:07.385401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06186df9fc17'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('interval', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(), nullable=True),
    sa.Column('transcription', sa.String(), nullable=True),
    sa.Column('ukr_translation', sa.String(), nullable=True),
    sa.Column('rus_translation', sa.String(), nullable=True),
    sa.Column('example_phrase', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'word_id', name='user_word')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_words')
    op.drop_table('words')
    op.drop_table('users')
    # ### end Alembic commands ###