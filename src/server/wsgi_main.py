"""An entry point for WSGI-based deployments of the Solar Power Monitor.

The application cannot accept command line arguments when executed in a WSGI
environment. Instead, application parameters are passed through by environment
variables.

For example, with Green Unicorn, the following command line runs the server and
queries a MySQL instance:

    $ gunicorn \
          -e UWSOLAR_DB_TYPE=mysql+mysqlconnector \
          -e UWSOLAR_DB_HOST=localhost \
          gunicorn_main:APP
"""
import os
import api_server
import db
import www_server


def create_app():
  """Creates a new application instance.

  Returns:
    A configured WSGI application instance.
  """
  # Get environment variables.
  www_path = os.environ.get('UWSOLAR_WWW_PATH', os.path.dirname(__file__) + '/www')
  db_type = os.environ.get('UWSOLAR_DB_TYPE', 'sqlite')
  db_user = os.environ.get('UWSOLAR_DB_USER', '')
  db_password = os.environ.get('UWSOLAR_DB_PASSWORD', '')
  db_host = os.environ.get('UWSOLAR_DB_HOST', 'sqlite.db')
  db_name = os.environ.get('UWSOLAR_DB_NAME', '')
  db_pool_size = os.environ.get('UWSOLAR_DB_POOL_SIZE', 0)

  # Initialize database connection.
  db_options = db.DatabaseOptions(db_type, db_user, db_password, db_host,
                                  db_name, db_pool_size)
  db_accessor = db.Database(db_options)

  # Create application instance.
  app = www_server.WwwServer(www_path).app()
  app.mount('/_/', api_server.ApiServer(db_accessor).app())
  return app


APP = create_app()
