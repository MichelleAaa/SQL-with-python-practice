"""add customers date_of_birth

Revision ID: aeaf86bedb44
Revises: 28cf156fc80b
Create Date: 2022-08-23 15:46:31.669310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeaf86bedb44'
down_revision = '28cf156fc80b'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE customers
        ADD COLUMN date_of_birth TIMESTAMP;
        """
    )



def downgrade():
    op.execute(
        """
        ALTER TABLE customers
        DROP COLUMN date_of_birth;
        """
    )

