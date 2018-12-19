"""Manages unit test access to database instances."""

import sqlalchemy
import db
import model


def create_engine(db_file):
  """Creates a new SQLAlchemy engine.

  The file is expected to be empty, and a new schema will be created within it.

  Args:
    db_file: The file containing SQLite database data.

  Returns:
    An engine object pointing to a SQLite database.
  """
  engine = sqlalchemy.create_engine('sqlite:///%s' % (db_file))
  model.BASE.metadata.create_all(engine)
  return engine


def create_accessor(db_file):
  """Creates a database accessor object.

  Args:
    db_file: The file containing SQLite database data.

  Returns:
    A database accessor object.
  """
  opts = db.DatabaseOptions('sqlite', None, None, db_file, None, None)
  return db.Database(opts)


def new_data(start, end, topic_id, value_string, delta):
  """Creates a series of data within a given range.

  Args:
    start: The start of the date range (inclusive).
    end: The end of the date range (inclusive).
    topic_id: The topic ID.
    value_string: The value string.

  Returns:
    A list of datum objects, evenly spaced apart in the given date range.
  """
  cur = start
  data = []
  while cur <= end:
    data.append(model.Datum(cur, topic_id, value_string))
    cur += delta

  return data
