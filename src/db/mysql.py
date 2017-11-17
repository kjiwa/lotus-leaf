"""A module containing a MySQL database connection handler."""

import datetime
import model
import mysql.connector


class MysqlDatabase(object):
  """A MySQL connection handler and data accessor."""

  def __init__(self, **kwargs):
    """Initializes a connection to the database.

    Detailed documentation for MySQL Connection/Python is available at
    https://dev.mysql.com/doc/connector-python/en/.

    Args:
      **kwargs: A dict of arguments for the MySQL connector.
    """
    self._db = mysql.connector.connect(**kwargs)

  def close(self):
    """Closes the database connection."""
    self._db.close()

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
