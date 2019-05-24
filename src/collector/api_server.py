"""The UW Solar API server."""

import collections
import datetime
import time
import bottle
from db import db_model

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

    self.init_topics()

    routes = [
      Route('GET', '/ping', ApiServer.ping),
      Route('GET', '/metric', self.get_metric),
      Route('POST', '/collect', self.collect)
    ]
    for route in routes:
      self._app.route(route.path, method=route.method, callback=route.callback)

  def app(self):
    """Returns a reference to the WSGI application."""
    return self._app

  def init_topics(self):
    """Adds the current panel connection's topics to the database if they don't already exist.

    If they do exist, do nothing.
    """
    topics_to_add = []
    panel_metrics = self._panel_con.metrics
    for metric in panel_metrics:
      topic_name = panel_metrics[metric].topic_name
      if not self._db_con.topic_exists(topic_name):
        # Set the id of the topic to be None. The responsibility of assigning an id
        # should be handled by the database.
        topic = db_model.Topic(None, topic_name)
        topics_to_add.append(topic)

    if topics_to_add:
      self._db_con.write_data(topics_to_add)

  @staticmethod
  def ping():
    """Returns a ping response.

    For now, this method always returns success as long as the server is
    active. In the future, this may be extended to perform more extensive
    health checks, such as to ensure that dependent services are available
    (e.g. the database and solar panel).
    """
    pass

  def get_metric(self):
    """Retrieves the value for a particular metric.

    Query string format:

      - name: The metric name.

    Returns:
      The current value of the metric.
    """
    name = bottle.request.query.get('name', None)
    if not name or not self._panel_con.has_metric(name):
      raise bottle.HTTPError(400)

    bottle.response.content_type = 'text/plain'
    return str(self._panel_con.get_metric(name))

  def collect(self):
    """Queries all known metrics and writes their values to the database.

    Query string format:

      - iterations: The number of times to query the metrics.
      - wait_time: The time in seconds to wait between iterations.

    It is expected that this method will be invoked periodically by a task
    scheduling service (e.g. cron). Cron specifically may invoke a task as
    frequently as once per minute. To collect data approximately once per
    second, the number of iterations may be set to 60 and the wait time may be
    set to 1.
    """
    iterations = bottle.request.query.get('iterations', '1')
    try:
      iterations = int(iterations)
    except ValueError:
      raise bottle.HTTPError(400)

    wait_time = bottle.request.query.get('wait_time', '1')
    try:
      wait_time = int(wait_time)
    except ValueError:
      raise bottle.HTTPError(400)

    # Map topic names to their IDs.
    topics = self._db_con.get_all_topics()
    topic_ids_by_name = {t.topic_name: t.topic_id for t in topics}

    # Query metrics.
    metrics = self._panel_con.metrics
    for _ in range(0, iterations):
      data = [db_model.TopicDatum(datetime.datetime.now(),
                                  topic_ids_by_name[m.topic_name],
                                  self._panel_con.get_metric(m.name))
              for m in metrics.values()]
      self._db_con.write_data(data)
      time.sleep(wait_time)
