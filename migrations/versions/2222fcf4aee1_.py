"""empty message

Revision ID: 2222fcf4aee1
Revises: 4cf6650e694f
Create Date: 2023-10-22 12:25:25.588677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2222fcf4aee1'
down_revision = '4cf6650e694f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dailyreport', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('sent_date', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(None, 'students', ['student_id'], ['student_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dailyreport', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('sent_date')
        batch_op.drop_column('student_id')

    # ### end Alembic commands ###