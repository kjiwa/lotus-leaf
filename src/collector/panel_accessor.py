"""A data accessor for network-connected solar panels.

This module uses the Modbus TCP protocol to connect to and read from solar
panels connected to the UW network. The configuration for these panels is
heterogeneous, so register mappings for each different configuration are
provided in Excel spreadsheets.
"""

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from collector import model

# A mapping from metric data type to decoding method.
DATA_TYPE_TO_DECODER_MAP = {
  model.MetricDataType.UINT8: BinaryPayloadDecoder.decode_8bit_uint,
  model.MetricDataType.UINT16: BinaryPayloadDecoder.decode_16bit_uint,
  model.MetricDataType.UINT32: BinaryPayloadDecoder.decode_32bit_uint,
  model.MetricDataType.UINT64: BinaryPayloadDecoder.decode_64bit_uint,
  model.MetricDataType.INT8: BinaryPayloadDecoder.decode_8bit_int,
  model.MetricDataType.INT16: BinaryPayloadDecoder.decode_16bit_int,
  model.MetricDataType.INT32: BinaryPayloadDecoder.decode_32bit_int,
  model.MetricDataType.INT64: BinaryPayloadDecoder.decode_64bit_int,
  model.MetricDataType.FLOAT32: BinaryPayloadDecoder.decode_32bit_float,
  model.MetricDataType.FLOAT64: BinaryPayloadDecoder.decode_64bit_float
}


class PanelAccessor:
  """A data accessor for solar panels."""

  def __init__(self, host, metrics):
    """Creates a new solar panel accessor.

    Args:
      host: The TCP host.
      metrics: A mapping of metric names to metric metadata for this panel.
    """
    self._modbus_client = ModbusTcpClient(host)
    self._metrics = metrics

  @property
  def metrics(self):
    return self._metrics

  def has_metric(self, name):
    """Checks if a particular metric is supported by this panel.

    Args:
      name: The metric name.

    Returns:
      Whether information about the metric is known.
    """
    return name in self._metrics

  def get_metric(self, name):
    """Gets the current value of a particular metric.

    This method queries the solar panel through its Modbus interface. The
    metric name is mapped to a Modbus address, and the registers at that
    address are retrieved and decoded.

    Args:
      name: The metric name.

    Returns:
      The current value of the metric.
    """
    metric = self._metrics[name]
    result = self._modbus_client.read_holding_registers(
      metric.address, metric.size, unit=0x01)

    decoder = BinaryPayloadDecoder.fromRegisters(result.registers)
    if metric.data_type == model.MetricDataType.STRING:
      return decoder.decode_string(metric.size * 8)

    return DATA_TYPE_TO_DECODER_MAP[metric.data_type](decoder)
