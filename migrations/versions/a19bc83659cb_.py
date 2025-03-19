"""empty message

Revision ID: a19bc83659cb
Revises: 45c9449643b4
Create Date: 2025-03-18 14:14:15.272974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a19bc83659cb'
down_revision: Union[str, None] = '45c9449643b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_item', sa.Column('product_id', sa.Integer(), nullable=False))
    op.drop_constraint('cart_item_product_it_fkey', 'cart_item', type_='foreignkey')
    op.create_foreign_key(None, 'cart_item', 'product', ['product_id'], ['id'])
    op.drop_column('cart_item', 'product_it')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_item', sa.Column('product_it', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'cart_item', type_='foreignkey')
    op.create_foreign_key('cart_item_product_it_fkey', 'cart_item', 'product', ['product_it'], ['id'])
    op.drop_column('cart_item', 'product_id')
    # ### end Alembic commands ###
