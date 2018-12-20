"""Object model definitions for solar panels."""

import collections
import enum


class MetricDataType(enum.Enum):
  """An enumeration of supported data types."""
  UNKNOWN = 0
  UINT8 = 1
  UINT16 = 2
  UINT32 = 3
  UINT64 = 4
  INT8 = 5
  INT16 = 6
  INT32 = 7
  INT64 = 8
  FLOAT32 = 9
  FLOAT64 = 10
  STRING = 11


# Metadata for a solar panel metric.
#
# Args:
#   name: The metric name.
#   description: A description of the metric.
#   address: The metric's Modbus address.
#   size: The number of registers used by the metric.
#   data_type: The metric data type.
#   topic_name: The topic name.
Metric = collections.namedtuple(
  'Metric', ['name', 'description', 'address', 'size', 'data_type',
             'topic_name'])
