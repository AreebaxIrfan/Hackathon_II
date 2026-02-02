"""Initial tables

Revision ID: 001
Revises:
Create Date: 2026-01-28 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('user',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tasks table
    op.create_table('task',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_completed', 'task', ['completed'])
    op.create_index('ix_task_created_at', 'task', ['created_at'])
    op.create_index('ix_user_created_at', 'user', ['created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_user_created_at', table_name='user')
    op.drop_index('ix_task_created_at', table_name='task')
    op.drop_index('ix_task_completed', table_name='task')
    op.drop_index('ix_task_user_id', table_name='task')

    # Drop tables
    op.drop_table('task')
    op.drop_table('user')