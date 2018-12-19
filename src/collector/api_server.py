"""The UW Solar API server."""

import collections
import bottle
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder

Route = collections.namedtuple('Route', ['method', 'path', 'callback'])


class ApiServer:
  """The UW Solar API server."""

  def __init__(self, db_accessor, modbus_host):
    """Initializes routes and the WSGI application.

    Args:
      db_accessor: The database accessor.
      modbus_host: The Modbus host address.
    """
    self._app = bottle.Bottle()
    self._db_accessor = db_accessor
    self._modbus_client = ModbusTcpClient(modbus_host)

    routes = [
      Route('GET', '/ping', ApiServer.ping),
      Route('GET', '/device_name', self.get_device_name)
    ]
    for route in routes:
      self._app.route(route.path, method=route.method, callback=route.callback)

  def app(self):
    """Returns a reference to the WSGI application."""
    return self._app

  @staticmethod
  def ping():
    """Returns a ping response.

    For now, this method always returns success as long as the server is
    active. In the future, this may be extneded to perform more extensive
    health checks, such as to ensure that dependent services are available
    (e.g. the database).
    """
    pass

  def get_device_name(self):
    """Returns the name of the Modbus device."""
    result = self._modbus_client.read_holding_registers(0, 8, unit=0x01)
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers)
    name = decoder.decode_string(16).decode('utf-8')
    return name
