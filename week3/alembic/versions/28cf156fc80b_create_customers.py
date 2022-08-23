"""create customers

Revision ID: 28cf156fc80b
Revises: 
Create Date: 2022-08-23 15:36:05.195436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28cf156fc80b'
down_revision = None
branch_labels = None
depends_on = None

# Forward Migration
def upgrade():
    op.execute(
        """
        CREATE TABLE customers(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """
    )


# Rollback Migration
def downgrade():
    op.execute(
        """
        DROP TABLE customers;
        """
    )
