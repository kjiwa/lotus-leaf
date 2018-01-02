"""An entry point for Gunicorn-based deployments of the Solar Power Monitor.

The application cannot accept command line arguments when executed by Gunicorn.
Instead, application parameters are passed through by environment variables.

To connect to a local MySQL instance, use the following command line:

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
  db_type = os.environ.get('UWSOLAR_DB_TYPE', 'sqlite')
  db_user = os.environ.get('UWSOLAR_DB_USER', 'uwsolar_ro')
  db_password = os.environ.get('UWSOLAR_DB_PASSWORD', '')
  db_host = os.environ.get('UWSOLAR_DB_HOST', ':memory:')
  db_name = os.environ.get('UWSOLAR_DB_NAME', 'uwsolar')
  db_pool_size = os.environ.get('UWSOLAR_DB_POOL_SIZE', )

  # Initialize database connection.
  db_options = db.DatabaseOptions(db_type, db_user, db_password, db_host,
                                  db_name, db_pool_size)
  db_accessor = db.Database(db_options)

  # Create application instance.
  app = www_server.WwwServer().app()
  app.mount('/_/', api_server.ApiServer(db_accessor).app())
  return app


APP = create_app()
