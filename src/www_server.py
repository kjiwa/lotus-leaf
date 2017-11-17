"""A UW Solar web server."""

import collections
import os.path
import bottle

_WWW_PATH = os.path.dirname(__file__) + '/../www'

_Route = collections.namedtuple('_Route', ['method', 'path', 'callback'])


class WwwServer(object):
  """The UW Solar web server."""

  def __init__(self):
    """Initializes routes and WSGI application."""

    # Define web application routes.
    routes = [_Route('GET', '/index.html', WwwServer.index)]

    # Initialize the WSGI application.
    self._app = bottle.Bottle()
    for route in routes:
      self._app.route(route.path, method=route.method, callback=route.callback)

  def app(self):
    """Returns a reference to the WSGI application."""
    return self._app

  @staticmethod
  def index():
    """Returns the contents of index.html.

    Returns:
      An HTML document.
    """
    bottle.response.content_type = 'text/html'
    with open(_WWW_PATH + '/index.html', 'r') as f:
      return f.read()
