"""rename

Revision ID: f7598feb7076
Revises: 06186df9fc17
Create Date: 2020-07-10 19:24:38.329099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7598feb7076'
down_revision = '06186df9fc17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('explanation', sa.String(), nullable=True))
    op.drop_column('words', 'explanation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('words', sa.Column('explanation', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('words', 'explanation')
    # ### end Alembic commands ###
