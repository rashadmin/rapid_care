"""empty message

Revision ID: 7ad38df6da95
Revises: 47235f8237ef
Create Date: 2024-01-12 15:51:38.473331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ad38df6da95'
down_revision = '47235f8237ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('anonyuser',
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=True),
    sa.Column('bloodgroup', sa.Enum('a_positive', 'b_positive', 'ab_positive', 'o_positive', 'a_negative', 'b_negative', 'ab_negative', 'o_negative', name='bloodgroup'), nullable=True),
    sa.Column('genotype', sa.Enum('AA', 'AS', 'SS', 'SC', 'AC', name='genotype'), nullable=True),
    sa.Column('medical_history', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('username', name=op.f('pk_anonyuser'))
    )
    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('anony_user_id', sa.String(length=32), nullable=True))
        batch_op.alter_column('conversation_no',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(batch_op.f('fk_conversation_anony_user_id_anonyuser'), 'anonyuser', ['anony_user_id'], ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('conversation', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_conversation_anony_user_id_anonyuser'), type_='foreignkey')
        batch_op.alter_column('conversation_no',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('anony_user_id')

    op.drop_table('anonyuser')
    # ### end Alembic commands ###