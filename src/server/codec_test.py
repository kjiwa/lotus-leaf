"""Unit tests for the db module."""

import json
import unittest
import datetime
import codec
import model


class CodecTestCase(unittest.TestCase):
  """A test case for codec operations."""

  def test_encode_topic(self):
    """Encodes a Topic object and ensures it has the correct representation."""
    topic = model.Topic(18, 'New Topic')
    actual = json.loads(json.dumps(topic, cls=codec.TopicEncoder))
    expected = [18, 'New Topic']
    self.assertEqual(expected, actual)

  def test_encode_datum(self):
    """Encodes a Datum object and ensures it has the correct representation."""
    ts = datetime.datetime(2018, 1, 1)
    datum = model.Datum(ts, 18, 'value')
    actual = json.loads(json.dumps(datum, cls=codec.DatumEncoder))
    expected = [ts.isoformat(), 18, 'value']
    self.assertEqual(expected, actual)
