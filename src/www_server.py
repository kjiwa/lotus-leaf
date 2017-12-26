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
    routes = [
        _Route('GET', '/', WwwServer.root),
        _Route('GET', '/uwsolar.js', WwwServer.uwsolarjs),
        _Route('GET', '/uwsolar.js.map', WwwServer.uwsolarjsmap),
        _Route('GET', '/<:re:.*>', WwwServer.redirect)
    ]

    # Initialize the WSGI application.
    self._app = bottle.Bottle()
    for route in routes:
      self._app.route(route.path, method=route.method, callback=route.callback)

  def app(self):
    """Returns a reference to the WSGI application."""
    return self._app

  @staticmethod
  def root():
    """Returns the contents of index.html.

    Returns:
      An HTML document.
    """
    bottle.response.content_type = 'text/html'
    with open(_WWW_PATH + '/dist/index.html', 'r') as f:
      return f.read()

  @staticmethod
  def uwsolarjs():
    """Returns the contents of uwsolar.js.

    Returns:
      A JavaScript script.
    """
    bottle.response.content_type = 'application/javascript'
    with open(_WWW_PATH + '/dist/uwsolar.js', 'r') as f:
      return f.read()

  @staticmethod
  def uwsolarjsmap():
    """Returns the contents of uwsolar.js.map.

    Returns:
      A source map.
    """
    bottle.response.content_type = 'application/json'
    with open(_WWW_PATH + '/dist/uwsolar.js.map', 'r') as f:
      return f.read()

  @staticmethod
  def redirect():
    """Redirects unmatched requests to /."""
    bottle.redirect('/', 301)
