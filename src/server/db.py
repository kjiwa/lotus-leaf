"""A module containing a SQL database connection handler."""

import collections
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.sql.expression
import model

# An object containing database options.
DatabaseOptions = collections.namedtuple(
    'DatabaseOptions',
    ['db_type', 'user', 'password', 'host', 'database', 'pool_size'])


class Database(object):
  """A class for all SQL-based database connection handlers."""

  def __init__(self, opts):
    """Initializes the database handler."""
    if opts.db_type == 'sqlite':
      self.engine = sqlalchemy.create_engine(
          '%s:///%s' % (opts.db_type, opts.host))
      return

    self.engine = sqlalchemy.create_engine(
        '%s://%s:%s@%s/%s' % (opts.db_type, opts.user, opts.password,
                              opts.host, opts.database),
        pool_size=opts.pool_size)

  def get_data(self, topic_id, start_dt, end_dt, sample_rate):
    """Gets time-series data for a given topic and date range.

    NOTE: Sampling does not work when using a SQLite backend.

    Args:
      topic_id: The topic to query.
      start_dt: The start datetime.
      end_dt: The end datetime.
      sample_rate: A sample rate, between 0 and 1 inclusive.

    Returns:
      A list of time-series data objects.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = (s.query(model.Datum).filter(model.Datum.topic_id == topic_id)
              .filter(model.Datum.ts >= start_dt)
              .filter(model.Datum.ts <= end_dt)
              .filter(sqlalchemy.sql.functions.random() <= sample_rate).all())
    s.close()
    return result

  def get_earliest_data_timestamp(self):
    """Gets the earliest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = s.query(model.Datum).order_by(model.Datum.ts.asc())
    datum = result.first()
    s.close()
    return datum.ts

  def get_latest_data_timestamp(self):
    """Gets the latest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = s.query(model.Datum).order_by(model.Datum.ts.desc())
    datum = result.first()
    s.close()
    return datum.ts

  def get_all_topics(self):
    """Gets a list of topic values.

    Returns:
      A list of Topic objects.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = s.query(model.Topic).all()
    s.close()
    return result
