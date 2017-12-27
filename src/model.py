"""A module containing object used throughout the UW Solar application."""

import json
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class Metadata(BASE):
  """An object describes that known metadata for a particular Topic."""
  __tablename__ = 'meta'
  topic_id = Column(Integer, primary_key=True)
  md = Column('metadata', Text, primary_key=True)

class Topic(BASE):
  """An object that describes the name of a meter and an associated metric.

  For example, a meter may have the name "UW/Maple/eaton_meter" and metrics such
  as "Angle_I_A", "freq", "pf", etc. Its topics will have the forms:

    * UW/Maple/eaton_meter/Angle_I_A
    * UW/Maple/eaton_meter/freq
    * UW/Maple/eaton_meter/pf
  """
  __tablename__ = 'topics'
  topic_id = Column(Integer, primary_key=True)
  topic_name = Column(String(512))

  def __init__(self, topic_id, name):
    super()
    self.topic_id = topic_id
    self.name = name

class Datum(BASE):
  """An object containing the value for a given topic at a particular time."""
  __tablename__ = 'data'
  ts = Column(DateTime)
  topic_id = Column(Integer, primary_key=True)
  value_string = Column(Text)

class TopicEncoder(json.JSONEncoder):
  """A class that prepares objects for JSON encoding."""
  # pylint: disable=arguments-differ,method-hidden
  def default(self, obj):
    if isinstance(obj, Topic):
      return {
          'id': obj.topic_id,
          'name': obj.topic_name
      }

    return json.JSONEncoder.default(self, obj)
