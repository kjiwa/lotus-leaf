"""Gendata unit tests."""

import datetime
import unittest
import gendata


class GendataTestCase(unittest.TestCase):
  """A test case for gendata operations."""

  def test_config_from_json_empty(self):
    """Tests that an empty list is returned for empty configs."""
    cfg = []
    opts = gendata.config_options_from_json(cfg)
    self.assertEqual([], opts)

  def test_config_from_json(self):
    """Tests that a valid config list is returned."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name'
    }]

    actual = gendata.config_options_from_json(cfg)
    opts = GendataTestCase.default_data_options(
        datetime.datetime(2016, 1, 9, 19),
        datetime.datetime(2016, 1, 9, 21),
        1, 'Topic name')

    self.assertEqual([opts], actual)

  def test_config_from_json_no_start(self):
    """Tests that an error is raised when there is no start date."""
    cfg = [{
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name'
    }]

    try:
      gendata.config_options_from_json(cfg)
      self.fail('Expected a ValueError')
    except ValueError:
      # expected
      pass


  def test_config_from_json_no_end(self):
    """Tests that an error is raised when there is no end date."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name'
    }]

    try:
      gendata.config_options_from_json(cfg)
      self.fail('Expected a ValueError')
    except ValueError:
      # expected
      pass


  def test_config_from_json_no_topic_id(self):
    """Tests that an error is raised when there is topic ID."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_name': 'Topic name'
    }]

    try:
      gendata.config_options_from_json(cfg)
      self.fail('Expected a ValueError')
    except ValueError:
      # expected
      pass


  def test_config_from_json_no_topic_name(self):
    """Tests that an error is raised when there is no topic name."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1
    }]

    try:
      gendata.config_options_from_json(cfg)
      self.fail('Expected a ValueError')
    except ValueError:
      # expected
      pass

  def test_config_from_json_topic_id_override(self):
    """Tests that topic ID overrides take precedence."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name'
    }]

    expected = GendataTestCase.default_data_options(
        datetime.datetime(2016, 1, 9, 19),
        datetime.datetime(2016, 1, 9, 21),
        33, 'Topic name')

    actual = gendata.config_options_from_json(cfg, topic_id_override=33)
    self.assertEqual([expected], actual)

  def test_config_from_json_topic_name_override(self):
    """Tests that topic name overrides take precedence."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name'
    }]

    expected = GendataTestCase.default_data_options(
        datetime.datetime(2016, 1, 9, 19),
        datetime.datetime(2016, 1, 9, 21),
        1, 'Override')

    actual = gendata.config_options_from_json(cfg, topic_name_override='Override')
    self.assertEqual([expected], actual)

  def test_config_from_json_topic_sample_rate_override(self):
    """Tests that sample overrides take precedence."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name',
        'sample_rate': 0.1
    }]

    expected = gendata.DataOptions(
        datetime.datetime(2016, 1, 9, 19),
        datetime.datetime(2016, 1, 9, 21),
        1, 'Topic name',
        0.33,
        gendata.DEFAULT_PERIOD,
        gendata.DEFAULT_AMPLITUDE_COS,
        gendata.DEFAULT_AMPLITUDE_SIN,
        gendata.DEFAULT_AMPLITUDE_OFFSET,
        gendata.DEFAULT_SPREAD)
    actual = gendata.config_options_from_json(cfg, sample_rate_override=0.33)
    self.assertEqual([expected], actual)

  def test_config_from_json_spread_override(self):
    """Tests that spread overrides take precedence."""
    cfg = [{
        'start': '2016-01-09T19:00:00',
        'end': '2016-01-09T21:00:00',
        'topic_id': 1,
        'topic_name': 'Topic name',
        'spread': 0.1
    }]

    expected = gendata.DataOptions(
        datetime.datetime(2016, 1, 9, 19),
        datetime.datetime(2016, 1, 9, 21),
        1, 'Topic name',
        gendata.DEFAULT_SAMPLE_RATE,
        gendata.DEFAULT_PERIOD,
        gendata.DEFAULT_AMPLITUDE_COS,
        gendata.DEFAULT_AMPLITUDE_SIN,
        gendata.DEFAULT_AMPLITUDE_OFFSET,
        0.33)
    actual = gendata.config_options_from_json(cfg, spread_override=0.33)
    self.assertEqual([expected], actual)

  @staticmethod
  def default_data_options(start, end, topic_id, topic_name):
    """Creates a DataOptions object filled with as many defaults as possible.

    Args:
      start: The start datetime.
      end: The end datetime.
      topic_id: The topic ID.
      topic_name: The topic name.
    """
    return gendata.DataOptions(
        start, end, topic_id, topic_name,
        gendata.DEFAULT_SAMPLE_RATE,
        gendata.DEFAULT_PERIOD,
        gendata.DEFAULT_AMPLITUDE_COS,
        gendata.DEFAULT_AMPLITUDE_SIN,
        gendata.DEFAULT_AMPLITUDE_OFFSET,
        gendata.DEFAULT_SPREAD)


if __name__ == '__main__':
  unittest.main()
