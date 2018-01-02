"""Unit tests for the db module."""

import os
import sys
import tempfile
import unittest
import datetime
import sqlalchemy
import sqlalchemy.orm
import testdb


class DatabaseTestCase(unittest.TestCase):
  """A test case for database operations."""

  # pylint: disable=missing-docstring
  def setUp(self):
    _, self.db_file = tempfile.mkstemp()
    self.engine = testdb.create_engine(self.db_file)
    self.db_accessor = testdb.create_accessor(self.db_file)

  # pylint: disable=missing-docstring
  def tearDown(self):
    os.unlink(self.db_file)

  def test_all_topics_empty(self):
    topics = self.db_accessor.get_all_topics()
    self.assertEqual(0, len(topics))

  def test_all_topics(self):
    # Insert a sample topic.
    topic = testdb.new_topic(18, 'Sample Topic')
    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(topic)
    session.commit()

    # Query database and validate results.
    topics = self.db_accessor.get_all_topics()
    self.assertEqual(len(topics), 1)
    self.assertEqual(topic.topic_id, topics[0].topic_id)
    self.assertEqual(topic.topic_name, topics[0].topic_name)

    session.close()

  def test_earliest_data_timestamp(self):
    # Insert two data objects.
    first = testdb.new_datum(
        datetime.datetime(2018, 1, 1), 18, 'first value string')
    second = testdb.new_datum(
        datetime.datetime(2018, 1, 2), 18, 'second value string')

    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(first)
    session.add(second)
    session.commit()

    # Query database and validate results.
    dt = self.db_accessor.get_earliest_data_timestamp()
    self.assertNotEqual(first.ts, second.ts)
    self.assertEqual(dt, first.ts)
    self.assertNotEqual(dt, second.ts)

    session.close()

  def test_latest_data_timestamp(self):
    # Insert two data objects.
    first = testdb.new_datum(
        datetime.datetime(2018, 1, 1), 18, 'first value string')
    second = testdb.new_datum(
        datetime.datetime(2018, 1, 2), 18, 'second value string')

    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(first)
    session.add(second)
    session.commit()

    # Query database and validate results.
    dt = self.db_accessor.get_latest_data_timestamp()
    self.assertNotEqual(first.ts, second.ts)
    self.assertNotEqual(dt, first.ts)
    self.assertEqual(dt, second.ts)

    session.close()

  def test_earliest_data_timestamp_empty(self):
    dt = self.db_accessor.get_earliest_data_timestamp()
    self.assertIsNone(dt)

  def test_latest_data_timestamp_empty(self):
    dt = self.db_accessor.get_latest_data_timestamp()
    self.assertIsNone(dt)

  def test_data_empty(self):
    data = self.db_accessor.get_data(18, datetime.datetime(2018, 1, 1),
                                     datetime.datetime(2018, 1, 1), 1)
    self.assertEqual([], data)

  def test_data(self):
    # Generate 24 data points, one per hour.
    cur = datetime.datetime(2018, 1, 1)
    end = datetime.datetime(2018, 1, 1, 23, 59)
    expected = []
    while cur < end:
      expected.append(testdb.new_datum(cur, 18, 'value'))
      cur += datetime.timedelta(hours=1)

    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add_all(expected)
    session.commit()

    # Query half of the data set.
    start = end - datetime.timedelta(hours=12)
    actual = sorted(
        self.db_accessor.get_data(18, start, end, sys.maxsize),
        key=lambda d: d.ts)

    self.assertEqual(len(expected) / 2, len(actual))
    for i in range(0, 12):
      expected_ts = datetime.datetime(2018, 1, 1, i + 12)
      self.assertEqual(expected_ts, actual[i].ts)

    session.close()
