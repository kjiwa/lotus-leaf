#!/usr/bin/python3
"""A program that launches the UW Solar web server."""

import argparse
import logging
import api_server
import bottle
import www_server


def parse_arguments():
  """Parses command-line options.

  Returns:
    An object containing parsed program arguments.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--debug',
      action='store_true',
      help='Whether to run the server in debug mode.')
  parser.add_argument(
      '--log_level', default='WARNING', help='The logging threshold.')
  parser.add_argument(
      '--port',
      type=int,
      default=8080,
      help='The port on which to listen for requests.')
  return parser.parse_args()


def main():
  """Parses command-line arguments and initializes the server."""
  args = parse_arguments()

  # Initialize logging.
  logging.basicConfig(level=logging.getLevelName(args.log_level))

  # Initialize and start the web application.
  # TODO(kjiwa): Load configuration from a file and pass it to the server.
  app = www_server.WwwServer().app()
  app.mount('/_/', api_server.ApiServer().app())
  bottle.run(app=app, host='0.0.0.0', port=args.port, debug=args.debug)


if __name__ == '__main__':
  main()
