"""Gendata unit tests."""

import datetime
import unittest
import gendata


class GendataTestCase(unittest.TestCase):
  """A test case for gendata operations."""

  def test_config_options_from_json_empty(self):
    """Tests that an empty list is returned for empty configs."""
    cfg = []
    opts = gendata.config_options_from_json(cfg)
    self.assertEqual([], opts)

  def test_config_options_from_json(self):
    """Tests that a valid config list is returned."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name'
    }]

    actual = gendata.config_options_from_json(cfg)
    opts = gendata.DataOptions(
        datetime.datetime(2016, 1, 9, 19),
        datetime.datetime(2016, 1, 9, 21),
        1, 'Topic name',
        gendata.DEFAULT_SAMPLE_RATE,
        gendata.DEFAULT_PERIOD,
        gendata.DEFAULT_AMPLITUDE_COS, gendata.DEFAULT_AMPLITUDE_SIN,
        gendata.DEFAULT_AMPLITUDE_OFFSET,
        gendata.DEFAULT_SPREAD)

    self.assertEqual([opts], actual)


if __name__ == '__main__':
  unittest.main()
