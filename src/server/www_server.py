"""The UW Solar web server."""

import bottle
import server


class WwwServer(server.BaseServer):
  """The UW Solar web server."""

  def __init__(self, www_path):
    """Initializes routes and WSGI application.

    Args:
      www_path: The directory where web resources are stored.
    """
    super().__init__([
        server.Route('GET', '/', self.root),
        server.Route('GET', '/favicon.ico', self.faviconico),
        server.Route('GET', '/uwsolar.js', self.uwsolarjs),
        server.Route('GET', '/uwsolar.js.map', self.uwsolarjsmap),
        server.Route('GET', '/<:re:.*>', WwwServer.redirect)
    ])

    self._www_path = www_path

  @staticmethod
  def read_file(path, open_mode='r'):
    """Reads a file and returns its contents.

    Args:
      path: The path of the file to be read.
      open_mode: The mode to use when opening the file.

    Returns:
      A string containing the file contents.
    """
    with open(path, open_mode) as f:
      return f.read()

  def faviconico(self):
    """Returns the contents of favicon.ico.

    Returns:
      An icon image.
    """
    bottle.response.content_type = 'image/x-icon'
    return WwwServer.read_file(self._www_path + '/favicon.ico', open_mode='rb')

  def root(self):
    """Returns the contents of index.html.

    Returns:
      An HTML document.
    """
    bottle.response.content_type = 'text/html'
    return WwwServer.read_file(self._www_path + '/index.html')

  def uwsolarjs(self):
    """Returns the contents of uwsolar.js.

    Returns:
      A JavaScript script.
    """
    bottle.response.content_type = 'application/javascript'
    return WwwServer.read_file(self._www_path + '/uwsolar.js')

  def uwsolarjsmap(self):
    """Returns the contents of uwsolar.js.map.

    Returns:
      A source map.
    """
    bottle.response.content_type = 'application/json'
    return WwwServer.read_file(self._www_path + '/uwsolar.js.map')

  @staticmethod
  def redirect():
    """Redirects unmatched requests to /."""
    bottle.redirect('/', 301)
