"""episode key map for course version upgrades

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-29 10:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('episode_key_map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('old_version_id', sa.Integer(), nullable=False),
    sa.Column('old_code', sa.String(length=8), nullable=False),
    sa.Column('new_version_id', sa.Integer(), nullable=False),
    sa.Column('new_code', sa.String(length=8), nullable=False),
    sa.Column('episode_key', sa.String(length=32), nullable=False),
    sa.Column('approved_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['new_version_id'], ['course_versions.id'], ),
    sa.ForeignKeyConstraint(['old_version_id'], ['course_versions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('episode_key_map')
