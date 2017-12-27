"""The UW Solar API server."""

import collections
import bottle

Route = collections.namedtuple('_Route', ['method', 'path', 'callback'])


class BaseServer(object):
  """The server base class."""

  def __init__(self, routes):
    """Initializes routes and WSGI application.

    Args:
      routes: A list of HTTP method to class method mappings.
    """

    self._app = bottle.Bottle()
    for route in routes:
      self._app.route(route.path, method=route.method, callback=route.callback)

  def app(self):
    """Returns a reference to the WSGI application."""
    return self._app
