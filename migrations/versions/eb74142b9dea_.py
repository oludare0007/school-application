"""empty message

Revision ID: eb74142b9dea
Revises: 413ca9be5354
Create Date: 2023-10-17 13:36:52.092135

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eb74142b9dea'
down_revision = '413ca9be5354'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.alter_column('ref_no',
               existing_type=mysql.FLOAT(),
               type_=sa.String(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payment', schema=None) as batch_op:
        batch_op.alter_column('ref_no',
               existing_type=sa.String(length=100),
               type_=mysql.FLOAT(),
               nullable=False)

    # ### end Alembic commands ###