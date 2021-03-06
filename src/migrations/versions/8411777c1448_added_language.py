"""added language

Revision ID: 8411777c1448
Revises: f7598feb7076
Create Date: 2020-09-12 20:02:38.175392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8411777c1448'
down_revision = 'f7598feb7076'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('language', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'language')
    # ### end Alembic commands ###
