"""Add 2FA fields to User model

Revision ID: e0bf982a416a
Revises: 
Create Date: 2024-12-01 11:43:43.825534

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e0bf982a416a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='temp_user')
    op.drop_index('username', table_name='temp_user')
    op.drop_table('temp_user')
    op.drop_index('email', table_name='user')
    op.drop_index('username', table_name='user')
    op.drop_table('user')
    op.add_column('users', sa.Column('otp_secret', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('is_2fa_enabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_2fa_enabled')
    op.drop_column('users', 'otp_secret')
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64), nullable=False),
    sa.Column('email', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=120), nullable=False),
    sa.Column('password_hash', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'user', ['username'], unique=True)
    op.create_index('email', 'user', ['email'], unique=True)
    op.create_table('temp_user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=64), nullable=False),
    sa.Column('email', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=120), nullable=False),
    sa.Column('password_hash', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=512), nullable=True),
    sa.Column('verify_token', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=256), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), nullable=True),
    sa.Column('expires_at', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'temp_user', ['username'], unique=True)
    op.create_index('email', 'temp_user', ['email'], unique=True)
    # ### end Alembic commands ###
