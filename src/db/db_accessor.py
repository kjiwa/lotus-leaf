"""A module containing a SQL database connection handler."""

import collections
import sys
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.sql.expression
from db import db_model

SQLITE_MAX_INT = sys.maxsize

# An object containing database options.
DatabaseOptions = collections.namedtuple(
  'DatabaseOptions',
  ['db_type', 'user', 'password', 'host', 'database', 'pool_size'])


class DatabaseAccessor:
  """A class for all SQL-based database connection handlers."""

  def __init__(self, opts):
    """Initializes the database handler."""
    self.db_type = opts.db_type
    if opts.db_type == 'sqlite':
      dsn = '%s:///%s' % (opts.db_type, opts.host)
      self.engine = sqlalchemy.create_engine(dsn)
    else:
      dsn = '%s://%s:%s@%s/%s' % (opts.db_type, opts.user, opts.password,
                                  opts.host, opts.database)
      self.engine = sqlalchemy.create_engine(dsn, pool_size=opts.pool_size)

  def get_data(self, topic_ids, start_dt, end_dt, sample_rate):
    """Gets time-series data for the given topics and date range.

    NOTE: Sampling does not work when using a SQLite backend.

    Args:
      topic_ids: The topics to query.
      start_dt: The start datetime.
      end_dt: The end datetime.
      sample_rate: A sample rate, between 0 and 1 inclusive.

    Returns:
      A list of time-series data objects.
    """
    # MySQL's rand() method returns a decimal in the range [0, 1]. SQLite's
    # random() method returns an integer between
    # [-9223372036854775808, 9223372036854775807]. Since we expect the caller to
    # send us a decimal in [0, 1], convert it into something suitable for SQLite
    # queries.
    if self.db_type == 'sqlite':
      sample_rate = SQLITE_MAX_INT * 2 * (sample_rate - 0.5)

    s = sqlalchemy.orm.Session(self.engine)
    try:
      result = (s.query(db_model.TopicDatum).filter(
        db_model.TopicDatum.topic_id.in_(topic_ids))
                .filter(db_model.TopicDatum.ts >= start_dt)
                .filter(db_model.TopicDatum.ts <= end_dt)
                .filter(sqlalchemy.sql.functions.random() <= sample_rate).all())
      return result
    finally:
      s.close()

  def get_earliest_data_timestamp(self):
    """Gets the earliest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    s = sqlalchemy.orm.Session(self.engine)
    try:
      result = s.query(db_model.TopicDatum).order_by(
        db_model.TopicDatum.ts.asc())
      if result.count() == 0:
        return None

      datum = result.first()
      return datum.ts
    finally:
      s.close()

  def get_latest_data_timestamp(self):
    """Gets the latest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    s = sqlalchemy.orm.Session(self.engine)
    try:
      result = s.query(db_model.TopicDatum).order_by(
        db_model.TopicDatum.ts.desc())
      if result.count() == 0:
        return None

      datum = result.first()
      return datum.ts
    finally:
      s.close()

  def get_all_topics(self):
    """Gets a list of topic values.

    Returns:
      A list of Topic objects.
    """
    s = sqlalchemy.orm.Session(self.engine)
    try:
      result = s.query(db_model.Topic).all()
      return result
    finally:
      s.close()

  def write_data(self, data):
    """Writes a list of topic values to the database.

    Args:
      data: A list of topic values to be written.
    """
    s = sqlalchemy.orm.Session(self.engine)
    try:
      s.add_all(data)
    finally:
      s.close()
