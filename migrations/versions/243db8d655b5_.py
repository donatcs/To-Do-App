"""empty message

Revision ID: 243db8d655b5
Revises: a6820037ab6b
Create Date: 2022-05-16 21:37:50.236431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243db8d655b5'
down_revision = 'a6820037ab6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todo', type_='foreignkey')
    op.drop_column('todo', 'user_id')
    op.add_column('user', sa.Column('todo_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'todo', ['todo_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'todo_id')
    op.add_column('todo', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'todo', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###