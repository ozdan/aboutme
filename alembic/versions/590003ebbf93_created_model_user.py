"""Created model User

Revision ID: 590003ebbf93
Revises: 
Create Date: 2014-12-03 16:39:33.778165

"""

# revision identifiers, used by Alembic.
revision = '590003ebbf93'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('biography', sa.Text(), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('work', sa.String(length=50), nullable=True),
    sa.Column('education', sa.String(length=70), nullable=True),
    sa.Column('interest', sa.String(length=30), nullable=True),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
