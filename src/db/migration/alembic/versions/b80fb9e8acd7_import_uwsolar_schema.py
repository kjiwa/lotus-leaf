"""Import uwsolar schema.

Revision ID: b80fb9e8acd7
Revises:
Create Date: 2017-12-30 13:11:53.458998

"""
import sqlalchemy as sa
import sqlalchemy.dialects.mysql as samysql
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b80fb9e8acd7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  """Creates the initial uwsolar tables."""
  # volttron_table_definitions
  op.create_table(
      'volttron_table_definitions',
      sa.Column('table_id', sa.String(512), primary_key=True),
      sa.Column('table_name', sa.String(512), nullable=False),
      sa.Column('table_prefix', sa.String(512), default=None),
      mysql_engine='innodb',
      mysql_charset='latin1')

  # topics
  op.create_table(
      'topics',
      sa.Column('topic_id', sa.Integer, primary_key=True, autoincrement=True),
      sa.Column('topic_name', sa.String(512), nullable=False, unique=True),
      mysql_engine='innodb',
      mysql_charset='latin1')

  # meta
  op.create_table(
      'meta',
      sa.Column('topic_id', sa.Integer, primary_key=True, autoincrement=True),
      sa.Column('metadata', sa.Text, nullable=False),
      mysql_engine='innodb',
      mysql_charset='latin1')

  # data
  op.create_table(
      'data',
      sa.Column(
          'ts',
          samysql.TIMESTAMP(fsp=6),
          nullable=False,
          default=sa.func.current_timestamp(),
          onupdate=sa.func.current_timestamp),
      sa.Column('topic_id', sa.Integer, nullable=False),
      sa.Column('value_string', sa.Text, nullable=False),
      mysql_engine='innodb',
      mysql_charset='latin1')
  op.create_index('ts', 'data', ['ts', 'topic_id'], unique=True)
  op.create_index('data_idx', 'data', ['ts'])


def downgrade():
  """Drops the uwsolar tables."""
  op.drop_table('volttron_table_definitions')
  op.drop_table('topics')
  op.drop_table('meta')
  op.drop_table('data')
