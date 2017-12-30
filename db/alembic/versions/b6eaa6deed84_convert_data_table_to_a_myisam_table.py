"""Convert data table engine from InnoDB MyISAM.

Revision ID: b6eaa6deed84
Revises: b80fb9e8acd7
Create Date: 2017-12-30 14:11:04.007441

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b6eaa6deed84'
down_revision = 'b80fb9e8acd7'
branch_labels = None
depends_on = None


def upgrade():
  conn = op.get_bind()
  conn.execute('alter table data engine=myisam')


def downgrade():
  conn = op.get_bind()
  conn.execute('alter table data engine=innodb')
