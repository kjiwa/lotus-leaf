"""Convert tables character set from Latin-1 to UTF-8.

Revision ID: 2534585a9391
Revises: b6eaa6deed84
Create Date: 2017-12-30 14:16:15.929700

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '2534585a9391'
down_revision = 'b6eaa6deed84'
branch_labels = None
depends_on = None


def upgrade():
  """Converts table character sets from Latin-1 to UTF-8."""
  conn = op.get_bind()
  conn.execute(
      'alter table volttron_table_definitions convert to character set utf8')
  conn.execute('alter table topics convert to character set utf8')
  conn.execute('alter table meta convert to character set utf8')
  conn.execute('alter table data convert to character set utf8')


def downgrade():
  """Converts table character sets from UTF-8 to Latin-1."""
  conn = op.get_bind()
  conn.execute('alter table volttron_table_definitions set charset=latin1')
  conn.execute('alter table topics set charset=latin1')
  conn.execute('alter table meta set charset=latin1')
  conn.execute('alter table data charset=latin1')
