"""A program that launches the UW Solar web server.

This launcher should only be used for development purposes. It is not suitable
for production deployments. A WSGI container such as Green Unicorn or uWSGI, or
a PaaS such as Amazon Elastic Beanstalk or Google App Engine should be used to
deploy the application for production purposes.
"""

import argparse
import bottle
import logging
from collector import api_server, metrics_builder, panel_accessor
from db import db_accessor

DEFAULT_HTTP_SERVER_HOST = '0.0.0.0'
DEFAULT_HTTP_SERVER_PORT = 8080
DEFAULT_DB_TYPE = 'sqlite'
DEFAULT_DB_USER = 'uwsolar'
DEFAULT_DB_PASSWORD = ''
DEFAULT_DB_HOST = ':memory:'
DEFAULT_DB_NAME = 'uwsolar'
DEFAULT_DB_POOL_SIZE = 3
DEFAULT_PANEL_METRICS_WORKSHEET_NAME = 'Metrics'


def parse_arguments():
  """Parses command line options.

  Returns:
    An object containing parsed program arguments.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--debug', action='store_true',
    help='Whether to run the server in debug mode.')
  parser.add_argument(
    '--log_level', default='WARNING', help='The logging threshold.')

  # HTTP server arguments.
  http_group = parser.add_argument_group('http', 'HTTP server arguments.')
  http_group.add_argument(
    '--host', default=DEFAULT_HTTP_SERVER_HOST,
    help='The hostname to bind to when listening for requests.')
  http_group.add_argument(
    '--port', type=int, default=DEFAULT_HTTP_SERVER_PORT,
    help='The port on which to listen for requests.')

  # Database connectivity arguments.
  db_group = parser.add_argument_group(
    'database', 'Database connectivity arguments.')
  db_group.add_argument(
    '--db_type', choices=['mysql+mysqlconnector', 'sqlite'],
    default=DEFAULT_DB_TYPE, help='Which database type should be used.')
  db_group.add_argument(
    '--db_user', default=DEFAULT_DB_USER, help='The database user.')
  db_group.add_argument(
    '--db_password', default=DEFAULT_DB_PASSWORD, help='The database password.')
  db_group.add_argument(
    '--db_host', default=DEFAULT_DB_HOST, help='The database host.')
  db_group.add_argument(
    '--db_name', default=DEFAULT_DB_NAME, help='The database name.')
  db_group.add_argument(
    '--db_pool_size', type=int, default=DEFAULT_DB_POOL_SIZE,
    help='The database pool size.')

  # Solar panel connectivity arguments.
  panel_group = parser.add_argument_group(
    'panel', 'Solar panel connectivity arguments.')
  panel_group.add_argument(
    '--panel_host', required=True, help='The solar panel host address.')
  panel_group.add_argument(
    '--panel_topic_prefix', required=True,
    help='The solar panel topic prefix (e.g. UW/Mercer).')
  panel_group.add_argument(
    '--panel_metrics_workbook', required=True,
    help='The workbook containing solar panel metrics data.')
  panel_group.add_argument(
    '--panel_metrics_worksheet_name',
    default=DEFAULT_PANEL_METRICS_WORKSHEET_NAME,
    help='The name of the worksheet containing metrics data.')

  return parser.parse_args()


def main():
  """Parses command line arguments and initilizes the server."""
  args = parse_arguments()
  logging.basicConfig(level=logging.getLevelName(args.log_level))

  # Initialize database connection.
  db_opts = db_accessor.DatabaseOptions(
    args.db_type, args.db_user, args.db_password, args.db_host, args.db_name,
    args.db_pool_size)
  db_con = db_accessor.DatabaseAccessor(db_opts)

  # Initialize solar panel connection.
  panel_metrics = metrics_builder.build_metrics(
    args.panel_metrics_workbook, args.panel_metrics_worksheet_name,
    args.panel_topic_prefix)
  panel_con = panel_accessor.PanelAccessor(args.panel_host, panel_metrics)

  # Initialize and run API server.
  app = api_server.ApiServer(db_con, panel_con).app()
  bottle.run(app=app, host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
  main()
