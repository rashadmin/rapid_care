"""empty message

Revision ID: bbd6e4e9d3e8
Revises: 7ad38df6da95
Create Date: 2024-01-12 17:17:51.328087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbd6e4e9d3e8'
down_revision = '7ad38df6da95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('anonyuser', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=36),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('anonyuser', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.String(length=36),
               type_=sa.VARCHAR(length=25),
               existing_nullable=False)

    # ### end Alembic commands ###