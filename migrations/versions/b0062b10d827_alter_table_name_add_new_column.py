"""Alter table name Add new column

Revision ID: b0062b10d827
Revises: 866374582c79
Create Date: 2025-07-01 00:03:15.681099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b0062b10d827'
down_revision: Union[str, Sequence[str], None] = '866374582c79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # # 1. Rename table from 'test' to 'test2'
    # op.rename_table('projected_parameters', 'variables_metadata')
    
    # # 2. Add a new column 'asemble' to 'test2'
    # op.add_column('variables_metadata', sa.Column('ensemble', sa.String(50), nullable=True))
    
    # 3. Rename column 'col1' to 'col2' in 'test2'
    op.alter_column('variables_metadata', 'parameter', new_column_name='variable', existing_type=sa.String(50))
    # ### end Alembic commands ###

