"""Gendata database unit tests."""

import datetime
import os
import tempfile
import unittest
import sqlalchemy.orm
import gendata
import model
import testdb


class GendataDbTestCase(unittest.TestCase):
  """A test case for gendata database operations."""

  def setUp(self):
    """Creates a temporary file for data storage and creates a server instance."""
    _, self.db_file = tempfile.mkstemp()
    self.engine = testdb.create_engine(self.db_file)

  def tearDown(self):
    """Removes the temporary database file."""
    os.unlink(self.db_file)

  def test_write_to_db(self):
    """Test that topics and data can be written to the DB."""
    # Create one topic and one datum to be created.
    ts = datetime.datetime.now()
    self.write_to_db([], [model.Topic(1, 'Topic')], [model.Datum(ts, 1, '1.0')])

    # Verify the items were written.
    session = sqlalchemy.orm.Session(bind=self.engine, expire_on_commit=False)
    actual_topics = session.query(model.Topic).all()
    actual_data = session.query(model.Datum).all()

    self.assertEqual(1, len(actual_topics))
    self.assertEqual(1, len(actual_data))

    topic = actual_topics[0]
    self.assertEqual(1, topic.topic_id)
    self.assertEqual('Topic', topic.topic_name)

    datum = actual_data[0]
    self.assertEqual(ts, datum.ts)
    self.assertEqual(1, datum.topic_id)
    self.assertEqual('1.0', datum.value_string)
    session.close()

  def write_to_db(self, options, topics, data):
    """Wraps gendata.write_to_db and transforms topic and data inputs.

    Args:
      options: The data generation options.
      topics: Topics to be written.
      data: Data to be written.
    """
    topics_map = dict((t.topic_id, t) for t in topics)
    data_map = dict((d.ts, d) for d in data)
    args = type('CommandLineArguments', (object, ), {
        'db_type': 'sqlite',
        'db_host': self.db_file
    })

    gendata.write_to_db(args, options, topics_map, data_map)
