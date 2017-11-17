"""The UW Solar API server."""

import collections
import json
import bottle

_Route = collections.namedtuple('_Route', ['method', 'path', 'callback'])


class ApiServer(object):
  """The UW Solar API server."""

  def __init__(self, db):
    """Initializes routes and WSGI application.

    Args:
      db: A database accessor.
    """

    self._db = db
    self._app = bottle.Bottle()

    # Define web application routes.
    routes = [
        _Route('GET', '/ping', ApiServer.ping),
        _Route('GET', '/data/dates', self.get_all_data_dates),
        _Route('GET', '/data/timestamp/earliest',
               self.get_latest_data_timestamp),
        _Route('GET', '/data/timestamp/latest',
               self.get_earliest_data_timestamp),
        _Route('GET', '/meta', self.get_all_metadata),
        _Route('GET', '/topics', self.get_all_topics)
    ]

    for route in routes:
      self._app.route(route.path, method=route.method, callback=route.callback)

  def app(self):
    """Returns a reference to the WSGI application."""
    return self._app

  @staticmethod
  def ping():
    """Returns a ping response.

    For now, this method always returns success as long as the web server was
    successfully initialized. In the future, this may be extended to perform
    more extensive health checks, such as to ensure that dependent services are
    available (e.g. the database).
    """
    pass

  def get_all_metadata(self):
    """Returns a list of all metadata values.

    A JSON-encoded list of metadata values.
    """
    bottle.response.content_type = 'application/json'
    return json.dumps(self._db.get_all_metadata())

  def get_all_topics(self):
    """Returns a list of topic values.

    Returns:
      A JSON-encoded list of topic values.
    """
    bottle.response.content_type = 'application/json'
    return json.dumps(self._db.get_all_topics())

  def get_all_data_dates(self):
    """Returns a list of dates for which there is solar panel activity.

    Warning: This API is very slow. Use sparingly.

    Returns:
      A JSON-encoded list of ISO8601 dates.
    """
    bottle.response.content_type = 'application/json'
    return json.dumps([i.isoformat() for i in self._db.get_all_data_dates()])

  def get_earliest_data_timestamp(self):
    """Returns the earliest timestamp for which there is solar panel activity.

    Returns:
      A JSON-encoded ISO8601 timestamp.
    """
    bottle.response.content_type = 'application/json'
    return json.dumps(self._db.get_earliest_data_timestamp().isoformat())

  def get_latest_data_timestamp(self):
    """Returns the latest timestamp for which there is solar panel activity.

    Returns:
      A JSON-encoded ISO8601 timestamp.
    """
    bottle.response.content_type = 'application/json'
    return json.dumps(self._db.get_latest_data_timestamp().isoformat())
