"""A data accessor for network-connected solar panels.

This module uses the Modbus TCP protocol to connect to and read from solar panels connected to the UW network. The
configuration for these panels is heterogeneous, so register mappings for each different configuration are provided in
Excel spreadsheets.
"""

import collections
import enum
import functools
import openpyxl
from . import settings
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


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
Metric = collections.namedtuple(
    'Metric', ['name', 'description', 'address', 'size', 'scaling_factor', 'data_type', 'topic_name'])

# The number of bits per register (2 bytes = 16 bits).
BITS_PER_REGISTER = 16

# A mapping from metric data type to decoding method.
DATA_TYPE_TO_DECODER_MAP = {
    MetricDataType.UINT8: BinaryPayloadDecoder.decode_8bit_uint,
    MetricDataType.UINT16: BinaryPayloadDecoder.decode_16bit_uint,
    MetricDataType.UINT32: BinaryPayloadDecoder.decode_32bit_uint,
    MetricDataType.UINT64: BinaryPayloadDecoder.decode_64bit_uint,
    MetricDataType.INT8: BinaryPayloadDecoder.decode_8bit_int,
    MetricDataType.INT16: BinaryPayloadDecoder.decode_16bit_int,
    MetricDataType.INT32: BinaryPayloadDecoder.decode_32bit_int,
    MetricDataType.INT64: BinaryPayloadDecoder.decode_64bit_int,
    MetricDataType.FLOAT32: BinaryPayloadDecoder.decode_32bit_float,
    MetricDataType.FLOAT64: BinaryPayloadDecoder.decode_64bit_float
}

# Data type mappings.
DATA_TYPE_STR_TO_ENUM = {
    'UINT8': MetricDataType.UINT8,
    'UINT16': MetricDataType.UINT16,
    'UINT32': MetricDataType.UINT32,
    'UINT64': MetricDataType.UINT64,
    'INT8': MetricDataType.INT8,
    'INT16': MetricDataType.INT16,
    'INT32': MetricDataType.INT32,
    'INT64': MetricDataType.INT64,
    'FLOAT32': MetricDataType.FLOAT32,
    'FLOAT64': MetricDataType.FLOAT64
}


@functools.lru_cache()
def client():
    """Builds a panel client with metrics information taken from an Excel workbook.

    Args:
        host: The panel TCP host.
        input_workbook: The Excel workbook containing metrics information.
        metrics_worksheet_name: The name of the worksheet containing data.
        topic_name_prefix: The topic name prefix.

    Returns:
        A dict from the metric name to its metadata.
    """

    def load_metric(row, topic_name_prefix):
        name = row[0].value
        if not name:
            return

        description = row[1].value
        address = row[2].value
        size = row[3].value
        scaling_factor = row[4].value
        data_type = DATA_TYPE_STR_TO_ENUM[row[5].value]
        topic_name = '{}/{}'.format(topic_name_prefix, name)
        return Metric(name, description, address, size, scaling_factor, data_type, topic_name)

    wb = openpyxl.load_workbook(settings.COLLECTOR_METRICS_INPUT_WORKBOOK, data_only=True, read_only=True)
    ws = wb[settings.COLLECTOR_METRICS_WORKSHEET_NAME]
    metrics = {}
    for r in ws.iter_rows(row_offset=1):
        metric = load_metric(r, settings.COLLECTOR_METRICS_TOPIC_NAME_PREFIX)
        metrics[metric.name] = metric

    return PanelAccessor(settings.COLLECTOR_PANEL_HOST, metrics)


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

        This method queries the solar panel through its Modbus interface. The metric name is mapped to a Modbus
        address, and the registers at that address are retrieved and decoded.

        Args:
            name: The metric name.

        Returns:
            The current value of the metric.
        """
        metric = self._metrics[name]
        result = self._modbus_client.read_holding_registers(metric.address, metric.size, unit=0x01)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        decoded_value = DATA_TYPE_TO_DECODER_MAP[metric.data_type](decoder)
        return decoded_value * metric.scaling_factor
