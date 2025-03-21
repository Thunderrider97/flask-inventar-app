"""Fix password_hash length

Revision ID: 3e818e1f6602
Revises: 90e7dea1533e
Create Date: 2025-03-21 22:51:56.950737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3e818e1f6602'
down_revision = '90e7dea1533e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               type_=sa.String(length=512),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=512),
               type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=128),
               existing_nullable=False)

    # ### end Alembic commands ###
