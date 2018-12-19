"""Executes a database migration."""

import argparse
from alembic import config


def parse_arguments():
  """Parses command line arguments.

  Returns:
    An object containing program options.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('--config_file', default='alembic.ini',
                      help='The alembic config filename.')
  parser.add_argument('--revision', default='head',
                      help='The revision to which to upgrade.')
  parser.add_argument('--db_type', default='sqlite',
                      help='The type of database to use.')
  parser.add_argument('--db_user', default='uwsolar', help='The database user.')
  parser.add_argument('--db_password', default='',
                      help='The database password.')
  parser.add_argument('--db_host', default=':memory:',
                      help='The database host.')
  parser.add_argument('--db_name', default='uwsolar', help='The database name.')
  return parser.parse_args()


def main():
  """Loads migration configuration and executes an upgrade."""
  args = parse_arguments()
  argv = ['-c', args.config_file,
          '-x', 'db_type=' + args.db_type,
          '-x', 'db_user=' + args.db_user,
          '-x', 'db_password=' + args.db_password,
          '-x', 'db_host=' + args.db_host,
          '-x', 'db_name=' + args.db_name,
          'upgrade', args.revision]
  config.main(argv)


if __name__ == '__main__':
  main()
