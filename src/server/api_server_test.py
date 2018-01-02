"""Unit tests for the API server module."""

import datetime
import json
import os
import tempfile
import unittest
import sqlalchemy
import boddle
import bottle
import api_server
import model
import testdb


class ApiServerTestCase(unittest.TestCase):
  """A test case for API server operations."""

  def setUp(self):
    """Creates a temporary file for data storage and creates a server instance."""
    _, self.db_file = tempfile.mkstemp()
    self.engine = testdb.create_engine(self.db_file)
    self.server = api_server.ApiServer(testdb.create_accessor(self.db_file))

  def tearDown(self):
    """Removes the temporary database file."""
    os.unlink(self.db_file)

  def test_all_topics_empty(self):
    """Tests that an empty list is returned when there are no topics."""
    actual = json.loads(self.server.get_all_topics())
    expected = []
    self.assertEqual(expected, actual)

  def test_all_topics(self):
    """Tests that all topics in the DB are returned."""
    # Insert a sample topic.
    topic = model.Topic(18, 'Sample Topic')
    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(topic)
    session.commit()

    # Query server and validate results.
    actual = json.loads(self.server.get_all_topics())
    expected = [[18, 'Sample Topic']]
    self.assertEqual(expected, actual)

    session.close()

  def test_earliest_data_timestamp(self):
    """Tests that the earliest known timestamp in the DB is returned."""
    # Insert two data objects.
    first = model.Datum(
        datetime.datetime(2018, 1, 1), 18, 'first value string')
    second = model.Datum(
        datetime.datetime(2018, 1, 2), 18, 'second value string')

    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(first)
    session.add(second)
    session.commit()

    # Query server and validate results.
    dt = json.loads(self.server.get_earliest_data_timestamp())
    self.assertNotEqual(first.ts, second.ts)
    self.assertEqual(dt, first.ts.isoformat())
    self.assertNotEqual(dt, second.ts.isoformat())

    session.close()

  def test_latest_data_timestamp(self):
    """Tests that the most recent known timestamp in the DB is returned."""
    # Insert two data objects.
    first = model.Datum(
        datetime.datetime(2018, 1, 1), 18, 'first value string')
    second = model.Datum(
        datetime.datetime(2018, 1, 2), 18, 'second value string')

    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(first)
    session.add(second)
    session.commit()

    # Query database and validate results.
    dt = json.loads(self.server.get_latest_data_timestamp())
    self.assertNotEqual(first.ts, second.ts)
    self.assertNotEqual(dt, first.ts.isoformat())
    self.assertEqual(dt, second.ts.isoformat())

    session.close()

  def test_earliest_data_timestamp_empty(self):
    """Test that nothing is returned when no data is in the DB."""
    dt = self.server.get_earliest_data_timestamp()
    self.assertEqual('', dt)

  def test_latest_data_timestamp_empty(self):
    """Test that nothing is returned when no data is in the DB."""
    dt = self.server.get_latest_data_timestamp()
    self.assertEqual('', dt)

  def test_data_empty(self):
    """Tests that an empty list is returned when there is no data in the DB."""
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=1)
    params = {
        'start_date_time': start.isoformat(),
        'end_date_time': end.isoformat(),
        'topic_id': '18',
        'sample_rate': '1'
    }

    with boddle.boddle(params=params):
      data = json.loads(self.server.get_data())

    self.assertEqual([], data)

  def test_data(self):
    """Tests that the correct amount of data is returned."""
    # Generate 24 data points, one per hour.
    start = datetime.datetime(2018, 1, 1)
    end = datetime.datetime(2018, 1, 1, 23, 59)
    expected = testdb.new_data(
        start, end, 18, 'value', datetime.timedelta(hours=1))

    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add_all(expected)
    session.commit()

    # Query half of the data set.
    start = end - datetime.timedelta(hours=12)
    params = {
        'start_date_time': start.isoformat(),
        'end_date_time': end.isoformat(),
        'topic_id': '18',
        'sample_rate': '1'
    }

    with boddle.boddle(params=params):
      actual = json.loads(self.server.get_data())

    self.assertEqual(len(expected) / 2, len(actual))
    for i in range(0, 12):
      expected = [
          datetime.datetime(2018, 1, 1, i + 12).isoformat(), 18, 'value'
      ]
      self.assertEqual(expected, actual[i])

    session.close()

  def test_data_no_topic_id(self):
    """Tests that an error occurs when there is no topic ID present."""
    params = {
        'start_date_time': datetime.datetime.now().isoformat(),
        'end_date_time': datetime.datetime.now().isoformat(),
        'sample_rate': '1'
    }

    try:
      with boddle.boddle(params=params):
        self.server.get_data()

      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass

  def test_data_no_start_date(self):
    """Tests that an error occurs when there is no start date present."""
    params = {
        'end_date_time': datetime.datetime.now().isoformat(),
        'topic_id': '18',
        'sample_rate': '1'
    }

    try:
      with boddle.boddle(params=params):
        self.server.get_data()

      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass

  def test_data_no_end_date(self):
    """Tests that an error occurs when there is no end date present."""
    params = {
        'start_date_time': datetime.datetime.now().isoformat(),
        'topic_id': '18',
        'sample_rate': '1'
    }

    try:
      with boddle.boddle(params=params):
        self.server.get_data()

      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass

  def test_data_no_sample_rate(self):
    """Tests that an error occurs when there is no sample rate present."""
    params = {
        'start_date_time': datetime.datetime.now().isoformat(),
        'end_date_time': datetime.datetime.now().isoformat(),
        'topic_id': '18'
    }

    try:
      with boddle.boddle(params=params):
        self.server.get_data()

      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass
