from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from collector import model

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
  def __init__(self, host, metrics):
    self._modbus_client = ModbusTcpClient(host)
    self._metrics = metrics

  def has_metric(self, name):
    return name in self._metrics

  def get_metric(self, name):
    metric = self._metrics[name]
    result = self._modbus_client.read_holding_registers(
      metric.address, metric.size, unit=0x01)

    decoder = BinaryPayloadDecoder.fromRegisters(result.registers)
    if metric.data_type == model.MetricDataType.STRING:
      return decoder.decode_string(metric.size * 8)

    return DATA_TYPE_TO_DECODER_MAP[metric.data_type](decoder)
