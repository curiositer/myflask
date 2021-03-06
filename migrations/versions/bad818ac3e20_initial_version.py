"""initial version

Revision ID: bad818ac3e20
Revises: 
Create Date: 2019-04-08 19:42:00.310778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad818ac3e20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contest',
    sa.Column('contest_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contest_name', sa.String(length=20), nullable=True),
    sa.Column('contest_type', sa.String(length=20), nullable=True),
    sa.Column('contest_time', sa.Date(), nullable=True),
    sa.Column('details', sa.String(length=150), nullable=True),
    sa.Column('level', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('contest_id')
    )
    op.create_table('team',
    sa.Column('team_id', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('team_name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('team_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('award',
    sa.Column('award_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=False),
    sa.Column('contest_id', sa.Integer(), nullable=True),
    sa.Column('grade', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['contest_id'], ['contest.contest_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('award_id')
    )
    op.create_table('request',
    sa.Column('request_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=False),
    sa.Column('contest_id', sa.Integer(), nullable=True),
    sa.Column('sup_teacher', sa.String(length=30), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.String(length=150), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contest_id'], ['contest.contest_id'], ),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_table('student',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('stu_class', sa.String(length=30), nullable=True),
    sa.Column('tel_num', sa.String(length=30), nullable=True),
    sa.Column('work_name', sa.String(length=30), nullable=True),
    sa.Column('work_type', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('teacher',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('stu_class', sa.String(length=30), nullable=True),
    sa.Column('tea_type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('team_student',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.team_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['student.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'team_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_student')
    op.drop_table('teacher')
    op.drop_table('student')
    op.drop_table('request')
    op.drop_table('award')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('team')
    op.drop_table('contest')
    # ### end Alembic commands ###
