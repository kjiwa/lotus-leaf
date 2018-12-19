"""A program that launches the UW Solar web server.

This launcher should only be used for development purposes. It is not suitable
for production deployments. A WSGI container such as Green Unicorn or uWSGI, or
a PaaS such as Amazon Elastic Beanstalk or Google App Engine should be used to
deploy the application for production purposes.
"""

import argparse
import bottle
import logging
from src import db
from src.collector import api_server


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
    '--host', default='0.0.0.0',
    help='The hostname to bind to when listening for requests.')
  http_group.add_argument(
    '--port', type=int, default=8080,
    help='The port on which to listen for requests.')

  # Database connectivity arguments.
  db_group = parser.add_argument_group(
    'database', 'Database connectivity arguments.')
  db_group.add_argument(
    '--db_type', choices=['mysql+mysqlconnector', 'sqlite'],
    default='sqlite', help='Which database type should be used.')
  db_group.add_argument(
    '--db_user', default='uwsolar', help='The database user.')
  db_group.add_argument(
    '--db_password', default='', help='The database password.')
  db_group.add_argument(
    '--db_host', default=':memory:', help='The database host.')
  db_group.add_argument(
    '--db_name', default='uwsolar', help='The database name.')
  db_group.add_argument(
    '--db_pool_size', type=int, default=3, help='The database pool size.')

  # Modbus connectivity arguments.
  modbus_group = parser.add_argument_group(
    'modbus', 'Modbus connectivity arguments.')
  modbus_group.add_argument(
    '--modbus_host', required=True, help='The Modbus host address.')

  return parser.parse_args()


def main():
  """Parses command line arguments and initilizes the server."""
  args = parse_arguments()
  logging.basicConfig(level=logging.getLevelName(args.log_level))

  db_options = db.DatabaseOptions(
    args.db_type, args.db_user, args.db_password, args.db_host, args.db_name,
    args.db_pool_size)
  db_accessor = db.Database(db_options)

  app = api_server.ApiServer(db_accessor, args.modbus_host).app()
  bottle.run(app=app, host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
  main()
