"""Add InventoryItem table

Revision ID: 90e7dea1533e
Revises: 473efc6826e6
Create Date: 2025-03-21 21:29:01.988227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90e7dea1533e'
down_revision = '473efc6826e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['list_id'], ['inventory_list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('inventory_field', schema=None) as batch_op:
        batch_op.alter_column('list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('field_type',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)

    with op.batch_alter_table('inventory_list', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)

    with op.batch_alter_table('inventory_list', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)

    with op.batch_alter_table('inventory_field', schema=None) as batch_op:
        batch_op.alter_column('field_type',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('list_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    op.drop_table('inventory_item')
    # ### end Alembic commands ###
