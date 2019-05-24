"""Object model definitions for solar panels."""

import dataclasses
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
#   size: The number of registers used by the metric. Each register is 2 bytes.
#   scaling_factor: The scaling factor to apply to the metric value.
#   data_type: The metric data type.
#   topic_name: The topic name.
@dataclasses.dataclass(frozen=True)
class Metric:
  name: str
  description: str
  address: int
  size: int
  scaling_factor: float
  data_type: str
  topic_name: str
