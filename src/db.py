"""A module containing a SQL database connection handlers."""

import abc
import collections
import datetime
import logging
import os.path
import sqlite3

import model
import mysql.connector

_SQLITE_SQL_PATH = os.path.dirname(__file__) + '/../test/db/'
_SQLITE_SQL = [
    'meta.sql', 'topics.sql', 'data.sql', 'volttron_table_definitions.sql'
]

LOGGER = logging.getLogger(__name__)

# An object containing database options.
DatabaseOptions = collections.namedtuple(
    'DatabaseOptions', ['user', 'password', 'host', 'database', 'pool_size'])


class AbstractSqlDatabase(abc.ABC):
  """An abstract base class for all SQL-based database connection handlers."""

  def __init__(self):
    """Initializes the database handler."""
    super()
    self._db = None

  def get_earliest_data_timestamp(self):
    """Gets the earliest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    result = None

    sql = 'select min(ts) from data'
    cursor = self._db.cursor()
    cursor.execute(sql)
    for (ts, ) in cursor:
      result = ts
      break

    cursor.close()
    return result

  def get_latest_data_timestamp(self):
    """Gets the latest timestamp from the data table.

    Returns:
      A datetime object for the latest data entry.
    """
    result = None

    sql = 'select max(ts) from data'
    cursor = self._db.cursor()
    cursor.execute(sql)
    for (ts, ) in cursor:
      result = ts
      break

    cursor.close()
    return result

  def get_all_data_dates(self):
    """Gets a list of unique dates for which there is solar panel data.

    Warning: This method results in a full table scan and is very expensive. Use
    sparingly.

    Returns:
      A list of dates.
    """
    timestamps = []

    sql = 'select distinct date_format(ts, "%d/%m/%Y") date from data'
    cursor = self._db.cursor()
    cursor.execute(sql)
    for (date, ) in cursor:
      timestamps.append(datetime.datetime.strptime(date, '%d/%m/%Y').date())

    cursor.close()
    return timestamps

  def get_all_metadata(self):
    """Gets a list of metadata values.

    Returns:
      A list of Meta objects.
    """
    meta = []

    sql = 'select topic_id, metadata from meta'
    cursor = self._db.cursor()
    cursor.execute(sql)
    for (topic_id, metadata) in cursor:
      meta.append(model.Metadata(topic_id, metadata))

    cursor.close()
    return meta

  def get_all_topics(self):
    """Gets a list of topic values.

    Returns:
      A list of Topic objects.
    """
    topics = []

    sql = 'select topic_id, topic_name from topics'
    cursor = self._db.cursor()
    cursor.execute(sql)
    for (topic_id, topic_name) in cursor:
      topics.append(model.Topic(topic_id, topic_name))

    cursor.close()
    return topics


class MysqlDatabase(AbstractSqlDatabase):
  """A MySQL connection handler and data accessor."""

  def __init__(self, options):
    """Initializes a connection to the database.

    Detailed documentation for MySQL Connection/Python is available at
    https://dev.mysql.com/doc/connector-python/en/.

    Args:
      options: An object containing database connectivity options.
    """
    super()

    dbconfig = {
        'user': options.user,
        'password': options.password,
        'host': options.host,
        'database': options.database,
        'pool_size': options.pool_size
    }

    self._db = mysql.connector.connect(**dbconfig)

  def __del__(self):
    """Releases the database connection."""
    self._db.close()


class SqliteDatabase(AbstractSqlDatabase):
  """A SQLite connection handler and data accessor."""

  def __init__(self, options):
    """Initializes a connection to the database.

    Args:
      options: An object containing database connectivity options.
    """
    super()

    self._db = sqlite3.connect(options.host)

    # Load sample data into the database when the in-memory option is chosen.
    if options.host == ':memory:':
      self._load_sample_data()

  def _load_sample_data(self):
    """Loads sample data into the database."""
    cursor = self._db.cursor()
    for sql in _SQLITE_SQL:
      with open(_SQLITE_SQL_PATH + sql, 'r') as f:
        try:
          cursor.executescript(f.read())
        except sqlite3.OperationalError as e:
          LOGGER.error('Unable to load data from ' + sql)
          raise e

    cursor.close()

  def __del__(self):
    """Releases the database connection."""
    self._db.close()

  def get_earliest_data_timestamp(self):
    """Gets the earliest timestamp for which there is data.

    This method is overridden because SQLite returns strings for timestamp
    fields. The result from the superclass is converted into a datetime object
    before being returned to the user.

    Returns:
      A datetime object.
    """
    result = super().get_earliest_data_timestamp()
    return datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f').date()

  def get_latest_data_timestamp(self):
    """Gets the latest timestamp for which there is data.

    This method is overridden because SQLite returns strings for timestamp
    fields. The result from the superclass is converted into a datetime object
    before being returned to the user.

    Returns:
      A datetime object.
    """
    result = super().get_latest_data_timestamp()
    return datetime.datetime.strptime(result, '%Y-%m-%d %H:%M:%S.%f').date()
