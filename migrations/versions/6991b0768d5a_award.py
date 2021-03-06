"""award

Revision ID: 6991b0768d5a
Revises: a812f85b7a69
Create Date: 2019-04-11 15:46:13.793886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6991b0768d5a'
down_revision = 'a812f85b7a69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('award', sa.Column('sup_teacher', sa.Integer(), nullable=True))
    op.drop_constraint('award_ibfk_2', 'award', type_='foreignkey')
    op.create_foreign_key(None, 'award', 'user', ['sup_teacher'], ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'award', type_='foreignkey')
    op.create_foreign_key('award_ibfk_2', 'award', 'user', ['user_id'], ['user_id'])
    op.drop_column('award', 'sup_teacher')
    # ### end Alembic commands ###
