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

    routes = [
      Route('GET', '/ping', ApiServer.ping),
      Route('GET', '/metric', self.get_metric),
      Route('POST', '/collect', self.collect),
      Route('POST', '/addtopic', self.add_topic),
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

  def add_topic(self):
    # On the situation where a new solar panel is introduced, this method
    # adds the corresponding topic names to the database.
    topic_names = [
      "Voltage_AN",
      "Voltage_BN",
      "Voltage_CN",
      "Current_N",
      "VA",
      "VAR",
      "W_A",
      "W_B",
      "W_C",
      "W",
      "freq",
      "pf_A",
      "pf_B",
      "pf_C",
      "pf",
      "Angle_V_AN",
      "Angle_V_BN",
      "Angle_V_CN",
      "Angle_I_A",
      "Angle_I_B",
      "Angle_I_C"
    ]

    meter_name = bottle.request.query.get('meter_name', None)
    if meter_name is None:
      raise bottle.HTTPError(400)

    data = [db_model.Topic(None, ("%s/%s") % (meter_name, topic)) for topic in topic_names]
    self._db_con.write_data(data)

    bottle.response.content_type = 'text/plain'
    return ("%s topics added.") % (len(data))
