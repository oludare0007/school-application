"""empty message

Revision ID: b352adb40cc4
Revises: 84564f939019
Create Date: 2023-10-14 07:29:06.974181

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b352adb40cc4'
down_revision = '84564f939019'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.alter_column('comments',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('result', schema=None) as batch_op:
        batch_op.alter_column('comments',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###
