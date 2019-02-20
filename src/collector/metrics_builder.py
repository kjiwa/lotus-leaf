"""Builds metrics information from an Excel file."""

import openpyxl
from collector import model

# Data type mappings.
DATA_TYPE_STR_TO_ENUM = {
  'UINT8': model.MetricDataType.UINT8,
  'UINT16': model.MetricDataType.UINT16,
  'UINT32': model.MetricDataType.UINT32,
  'UINT64': model.MetricDataType.UINT64,
  'INT8': model.MetricDataType.INT8,
  'INT16': model.MetricDataType.INT16,
  'INT32': model.MetricDataType.INT32,
  'INT64': model.MetricDataType.INT64,
  'FLOAT32': model.MetricDataType.FLOAT32,
  'FLOAT64': model.MetricDataType.FLOAT64
}


def build_metrics(input_workbook, metrics_worksheet_name, topic_name_prefix):
  """Builds metrics information from an Excel workbook.

  Args:
    input_workbook: The Excel workbook containing metrics information.
    metrics_worksheet_name: The name of the worksheet containing data.
    topic_name_prefix: The topic name prefix.

  Returns:
    A dict from the metric name to its metadata.
  """
  wb = openpyxl.load_workbook(input_workbook, data_only=True, read_only=True)
  ws = wb[metrics_worksheet_name]

  result = {}
  for row in ws.iter_rows(min_row=2):
    name = row[0].value
    if not name:
      break

    description = row[1].value
    address = row[2].value
    size = row[3].value
    scaling_factor = row[4].value
    data_type = DATA_TYPE_STR_TO_ENUM[row[5].value]
    topic_name = '{}/{}'.format(topic_name_prefix, name)
    result[name] = model.Metric(
      name, description, address, size, scaling_factor, data_type, topic_name)

  return result
