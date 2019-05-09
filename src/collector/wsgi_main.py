"""An entry point for WSGI-based deployments of the Solar Power Monitor.

The application cannot accept command line arguments when executed in a WSGI
environment. Instead, application parameters are passed through by environment
variables.

For example, with Green Unicorn, the following command line runs the server and
queries a MySQL instance:

    $ gunicorn \
          -e UWSOLAR_DB_TYPE=mysql+mysqlconnector \
          -e UWSOLAR_DB_HOST=localhost \
          -e UWSOLAR_PANEL_METRICS_WORKBOOK=maps/nexus-metrics.xlsx \
          -e UWSOLAR_PANEL_HOST=10.0.0.1 \
          -e UWSOLAR_PANEL_TOPIC_PREFIX=UW/Smithsonian/nexus_meter \
          gunicorn_main
"""
import os
from collector import api_server, metrics_builder, panel_accessor
from db import db_accessor


def create_app():
  """Creates a new application instance.

  Returns:
    A configured WSGI application instance.
  """
  # Database connectivity variables.
  db_type = os.environ.get('UWSOLAR_DB_TYPE', 'sqlite')
  db_user = os.environ.get('UWSOLAR_DB_USER', '')
  db_password = os.environ.get('UWSOLAR_DB_PASSWORD', '')
  db_host = os.environ.get('UWSOLAR_DB_HOST', 'sqlite.db')
  db_name = os.environ.get('UWSOLAR_DB_NAME', '')
  db_pool_size = os.environ.get('UWSOLAR_DB_POOL_SIZE', 0)

  # Solar panel connectivity variables.
  panel_metrics_workbook = os.environ.get('UWSOLAR_PANEL_METRICS_WORKBOOK')
  panel_metrics_worksheet_name = os.environ.get(
    'UWSOLAR_PANEL_METRICS_WORKSHEET_NAME', 'Metrics')
  panel_topic_prefix = os.environ.get('UWSOLAR_PANEL_TOPIC_PREFIX')
  panel_host = os.environ.get('UWSOLAR_PANEL_HOST')
  panel_modbus_retries = os.environ.get('UWSOLAR_PANEL_MODBUS_RETRIES', 3)
  panel_modbus_retry_wait_time = os.environ.get(
    'UWSOLAR_PANEL_MODBUS_RETRY_WAIT_TIME', 1)

  # Initialize database connection.
  db_opts = db_accessor.DatabaseOptions(db_type, db_user, db_password, db_host,
                                        db_name, db_pool_size)
  db_con = db_accessor.DatabaseAccessor(db_opts)

  # Initialize solar panel connection.
  panel_metrics = metrics_builder.build_metrics(
    panel_metrics_workbook, panel_metrics_worksheet_name, panel_topic_prefix)
  panel_con = panel_accessor.PanelAccessor(
    panel_host, panel_metrics, panel_modbus_retries,
    panel_modbus_retry_wait_time)

  # Create application instance.
  return api_server.ApiServer(db_con, panel_con).app()


application = create_app()
