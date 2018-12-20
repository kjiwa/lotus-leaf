"""A module containing database model definitions for the UW Solar application.

The object model for the UW Solar project is derived from the default schema
implemented by the VOLTTRON platform, which defines the following structures:

  * Topic: A particular solar panel property (e.g. V_AN, frequency, etc.)
  * Metadata: A map containing topic information (e.g. units or timezone).

A process (the collector) periodically queries a solar panel for its topic data
and writes it to the "data" table by creating a TopicDatum object.
"""

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class Metadata(BASE):
  """An object containing JSON-encoded metadata for a particular Topic.

  Each topic has one metadata object with the following properties:

    * units: The units associated with the topic data.
    * tz: The timezone to use when interpreting the topic data.
    * type: The type of data.

  Not all of these properties may be present for a given topic. The following
  table shows example metadata for a few different topics.

  Topic                          | Metadata
  -----------------------------------------------------------------------------
  UW/Maple/eaton_meter/Angle_I_A | {"units":"degrees","tz":"PT","type":"float"}
  UW/Maple/eaton_meter/freq      | {"units":"Hz","tz":"PT","type":"float"}
  UW/Maple/eaton_meter/pf        | {"units":"","tz":"PT","type":"float"}
  """
  __tablename__ = 'meta'
  topic_id = Column(Integer, primary_key=True)
  md = Column('metadata', Text, primary_key=True)


class Topic(BASE):
  """An object mapping the name of a meter and an associated metric.

  For example, a meter may have the name "UW/Maple/eaton_meter" and metrics such
  as "Angle_I_A", "freq", "pf", etc. Its topics will have the forms:

    * UW/Maple/eaton_meter/Angle_I_A
    * UW/Maple/eaton_meter/freq
    * UW/Maple/eaton_meter/pf
  """
  __tablename__ = 'topics'
  topic_id = Column(Integer, primary_key=True)
  topic_name = Column(String(512))

  def __init__(self, topic_id, topic_name):
    """Creates a new topic.

    Args:
      topic_id: The topic ID.
      topic_name: The topic name.
    """
    self.topic_id = topic_id
    self.topic_name = topic_name


class TopicDatum(BASE):
  """An object containing the value for a given topic at a particular time."""
  __tablename__ = 'data'
  ts = Column(DateTime, primary_key=True)
  topic_id = Column(Integer, primary_key=True)
  value_string = Column(Text, primary_key=True)

  def __init__(self, ts, topic_id, value_string):
    """Creates a new datum object.

    Args:
      ts: The timestamp.
      topic_id: The topic ID.
      value_string: The value string.
    """
    self.ts = ts
    self.topic_id = topic_id
    self.value_string = value_string
