"""The UW Solar API server."""

import collections
import bottle

Route = collections.namedtuple('Route', ['method', 'path', 'callback'])


class ApiServer:
  """The UW Solar API server."""

  def __init__(self, db_con, panel_con):
    """Initializes routes and the WSGI application.

    Args:
      db_con: A handle to the database.
      panel_con: A handle to the solar panel.
    """
    self._app = bottle.Bottle()
    self._db_con = db_con
    self._panel_con = panel_con

    routes = [
      Route('GET', '/ping', ApiServer.ping),
      Route('GET', '/metric', self.get_metric)
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
    (e.g. the database and solar panel).
    """
    pass

  def get_metric(self):
    """Retrieves the value for a particular metric.

    The metric name is expected to be provided in the query string.

    Returns:
      The current value of the metric.
    """
    name = bottle.request.query['name']
    if not name or not self._panel_con.has_metric(name):
      raise bottle.HTTPError(400)

    bottle.response.content_type = 'text/plain'
    return str(self._panel_con.get_metric(name))
