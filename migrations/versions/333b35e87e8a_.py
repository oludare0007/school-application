"""empty message

Revision ID: 333b35e87e8a
Revises: 
Create Date: 2023-10-04 22:42:10.012116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '333b35e87e8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('session', sa.String(length=100), nullable=False),
    sa.Column('school_fees', sa.Float(), nullable=False),
    sa.Column('books_fees', sa.Float(), nullable=False),
    sa.Column('uniform_fees', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    # ### end Alembic commands ###
