"""Manages unit test access to database instances."""

import sqlalchemy
import db
import model


def create_engine(db_file):
  engine = sqlalchemy.create_engine('sqlite:///%s' % (db_file))
  model.BASE.metadata.create_all(engine)
  return engine


def create_accessor(db_file):
  opts = db.DatabaseOptions('sqlite', None, None, db_file, None, None)
  return db.Database(opts)


def new_topic(topic_id, topic_name):
  topic = model.Topic()
  topic.topic_id = topic_id
  topic.topic_name = topic_name
  return topic


def new_datum(ts, topic_id, value_string):
  datum = model.Datum()
  datum.ts = ts
  datum.topic_id = topic_id
  datum.value_string = value_string
  return datum
