"""Unit tests for the API server module."""

import datetime
import json
import os
import tempfile
import unittest
import bottle
import sqlalchemy
import api_server
import testdb


class ApiServerTestCase(unittest.TestCase):
  """A test case for API server operations."""

  # pylint: disable=missing-docstring
  def setUp(self):
    _, self.db_file = tempfile.mkstemp()
    self.engine = testdb.create_engine(self.db_file)
    self.server = api_server.ApiServer(testdb.create_accessor(self.db_file))

  # pylint: disable=missing-docstring
  def tearDown(self):
    os.unlink(self.db_file)

  def test_all_topics_empty(self):
    actual = json.loads(self.server.get_all_topics())
    expected = []
    self.assertEqual(expected, actual)

  def test_all_topics(self):
    # Insert a sample topic.
    topic = testdb.new_topic(18, 'Sample Topic')
    session = sqlalchemy.orm.Session(bind=self.engine)
    session.add(topic)
    session.commit()

    # Query server and validate results.
    actual = json.loads(self.server.get_all_topics())
    expected = [[18, 'Sample Topic']]
    self.assertEqual(expected, actual)

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

    # Query server and validate results.
    dt = json.loads(self.server.get_earliest_data_timestamp())
    self.assertNotEqual(first.ts, second.ts)
    self.assertEqual(dt, first.ts.isoformat())
    self.assertNotEqual(dt, second.ts.isoformat())

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
    dt = json.loads(self.server.get_latest_data_timestamp())
    self.assertNotEqual(first.ts, second.ts)
    self.assertNotEqual(dt, first.ts.isoformat())
    self.assertEqual(dt, second.ts.isoformat())

    session.close()

  def test_earliest_data_timestamp_empty(self):
    dt = self.server.get_earliest_data_timestamp()
    self.assertEqual('', dt)

  def test_latest_data_timestamp_empty(self):
    dt = self.server.get_latest_data_timestamp()
    self.assertEqual('', dt)

  def test_data_empty(self):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(days=1)

    bottle.request.query['start_date_time'] = start.isoformat()
    bottle.request.query['end_date_time'] = end.isoformat()
    bottle.request.query['topic_id'] = '18'
    bottle.request.query['sample_rate'] = '1'
    data = json.loads(self.server.get_data())

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
    bottle.request.query['start_date_time'] = start.isoformat()
    bottle.request.query['end_date_time'] = end.isoformat()
    bottle.request.query['topic_id'] = '18'
    bottle.request.query['sample_rate'] = '1'
    actual = json.loads(self.server.get_data())

    self.assertEqual(len(expected) / 2, len(actual))
    for i in range(0, 12):
      expected = [
          datetime.datetime(2018, 1, 1, i + 12).isoformat(), 18, 'value'
      ]
      self.assertEqual(expected, actual[i])

    session.close()

  def test_data_no_topic_id(self):
    start = datetime.datetime.now()
    bottle.request.query['start_date_time'] = start.isoformat()
    bottle.request.query['end_date_time'] = start.isoformat()
    bottle.request.query['topic_id'] = None
    bottle.request.query['sample_rate'] = '1'
    try:
      self.server.get_data()
      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass

  def test_data_no_start_date(self):
    start = datetime.datetime.now()
    bottle.request.query['start_date_time'] = None
    bottle.request.query['end_date_time'] = start.isoformat()
    bottle.request.query['topic_id'] = '18'
    bottle.request.query['sample_rate'] = '1'
    try:
      self.server.get_data()
      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass

  def test_data_no_end_date(self):
    start = datetime.datetime.now()
    bottle.request.query['start_date_time'] = start.isoformat()
    bottle.request.query['end_date_time'] = None
    bottle.request.query['topic_id'] = '18'
    bottle.request.query['sample_rate'] = '1'
    try:
      self.server.get_data()
      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass

  def test_data_no_sample_rate(self):
    start = datetime.datetime.now()
    bottle.request.query['start_date_time'] = start.isoformat()
    bottle.request.query['end_date_time'] = start.isoformat()
    bottle.request.query['topic_id'] = '18'
    bottle.request.query['sample_rate'] = None
    try:
      self.server.get_data()
      self.fail('Expected a server error.')
    except bottle.HTTPError:
      # expected
      pass
