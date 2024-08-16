"""M

Revision ID: 96f9a3e7da73
Revises: 6114c5a23f6a
Create Date: 2024-08-16 07:59:36.687738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96f9a3e7da73'
down_revision = '6114c5a23f6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manufacturer_products', schema=None) as batch_op:
        batch_op.alter_column('manufacturer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('fk_manufacturer_products_manufacturer_id_manufacturers', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manufacturer_products', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_manufacturer_products_manufacturer_id_manufacturers', 'manufacturers', ['manufacturer_id'], ['id'])
        batch_op.alter_column('manufacturer_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###