"""modified student

Revision ID: 24598d5d8d9b
Revises: 7005ec988c5d
Create Date: 2019-04-19 15:34:51.612785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '24598d5d8d9b'
down_revision = '7005ec988c5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('after_major', sa.String(length=30), nullable=True))
    op.add_column('student', sa.Column('create_job', sa.String(length=30), nullable=True))
    op.add_column('student', sa.Column('create_type', sa.String(length=30), nullable=True))
    op.add_column('student', sa.Column('major_in', sa.String(length=30), nullable=True))
    op.drop_column('student', 'stu_class')
    op.drop_column('teacher', 'stu_class')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teacher', sa.Column('stu_class', mysql.VARCHAR(length=30), nullable=True))
    op.add_column('student', sa.Column('stu_class', mysql.VARCHAR(length=30), nullable=True))
    op.drop_column('student', 'major_in')
    op.drop_column('student', 'create_type')
    op.drop_column('student', 'create_job')
    op.drop_column('student', 'after_major')
    # ### end Alembic commands ###
