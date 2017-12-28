"""A UW Solar web server."""

import os.path
import bottle
import server

_WWW_PATH = os.path.dirname(__file__) + '/../../dist/www'


class WwwServer(server.BaseServer):
  """The UW Solar web server."""

  def __init__(self):
    """Initializes routes and WSGI application."""
    super().__init__([
        server.Route('GET', '/', WwwServer.root),
        server.Route('GET', '/uwsolar.js', WwwServer.uwsolarjs),
        server.Route('GET', '/uwsolar.js.map', WwwServer.uwsolarjsmap),
        server.Route('GET', '/<:re:.*>', WwwServer.redirect)
    ])

  @staticmethod
  def read_file(path):
    """Reads a file and returns its contents.

    Args:
      path: The path of the file to be read.

    Returns:
      A string containing the file contents.
    """
    with open(path, 'r') as f:
      return f.read()

  @staticmethod
  def root():
    """Returns the contents of index.html.

    Returns:
      An HTML document.
    """
    bottle.response.content_type = 'text/html'
    return WwwServer.read_file(_WWW_PATH + '/index.html')

  @staticmethod
  def uwsolarjs():
    """Returns the contents of uwsolar.js.

    Returns:
      A JavaScript script.
    """
    bottle.response.content_type = 'application/javascript'
    return WwwServer.read_file(_WWW_PATH + '/uwsolar.js')

  @staticmethod
  def uwsolarjsmap():
    """Returns the contents of uwsolar.js.map.

    Returns:
      A source map.
    """
    bottle.response.content_type = 'application/json'
    return WwwServer.read_file(_WWW_PATH + '/uwsolar.js.map')

  @staticmethod
  def redirect():
    """Redirects unmatched requests to /."""
    bottle.redirect('/', 301)
