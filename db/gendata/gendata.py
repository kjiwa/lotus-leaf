"""Generates and loads sample solar data.

The input is expected to be a JSON file containing a list of date ranges and
data generation options. This script generates sinusoidal data for each series,
according to the following expression:

  value = A_cos*cos(2*pi*t/period) + A_sin*sin(2*pi*t/period)

Since this expression is one term from the Fourier series, any desired curve can
be approximated by adding a sufficient number of time series options. See
sample-cos.json, sample-sawtooth.json, and sample-square.json for examples that
generate cosine, sawtooth, and square waves, respectively.

Options currently supported include:

  - start: The start of the date range, as an ISO-8601 string.
  - end: The end of the date range, as an ISO-8601 string.
  - topic_id: The topic ID for which data is being generated.
  - topic_name: The topic name for which data is being generated.
  - sample_rate: The number of samples to generate per second. Defaults to 0.01,
        or one sample every 100 seconds.
  - period: The sinusoid period in seconds. Defaults to 86400 (one day).
  - amplitude_cos: The cosine amplitude. Defaults to 0.
  - amplitude_sin: The sine amplitude. Defaults to 0.
  - amplitude_offset: The amplitude offset. Defaults to 0.
  - spread: A measure of how spread apart the data can be. Defaults to 0.05.

An example configuration that generates the line, y = 1 +/- 0.1, for one day is:

[
  {
    "start": "2017-12-30T00:00:00.0000Z",
    "end": "2017-12-30T23:59:59.99999Z",
    "topic_id": 14,
    "topic_name": "Test Topic #14",
    "amplitude_offset": 1,
    "spread": 0.1
  }
]
"""
import argparse
import collections
import datetime
import json
import logging
import math
import random
import dateutil.parser
import jsmin
import sqlalchemy
import model

DEFAULT_SAMPLE_RATE = 0.01
DEFAULT_PERIOD = 86400
DEFAULT_AMPLITUDE_COS = 0
DEFAULT_AMPLITUDE_SIN = 0
DEFAULT_AMPLITUDE_OFFSET = 0
DEFAULT_SPREAD = 0.05

DataOptions = collections.namedtuple('DataOptions', [
    'start', 'end', 'topic_id', 'topic_name', 'sample_rate', 'period',
    'amplitude_cos', 'amplitude_sin', 'amplitude_offset', 'spread'
])


def parse_arguments():
  """Parses command line arguments.

  Returns:
    An object containing parsed arguments.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--log_level', default='INFO', help='The logging threshold.')

  # Data generation arguments
  data_group = parser.add_argument_group('data', 'Data generation arguments.')
  data_group.add_argument(
      '--input_file',
      required=True,
      help='The input file containing data generation options.')
  data_group.add_argument(
      '--topic_id',
      type=int,
      help='Override the topic ID to use during data generation.')
  data_group.add_argument(
      '--topic_name',
      help='Override the topic name to use during data generation.')
  data_group.add_argument(
      '--sample_rate',
      type=float,
      help='Override the sample rate to use during data generation.')
  data_group.add_argument(
      '--spread',
      type=float,
      help='Override the spread to use during data generation.')

  # Database connectivity arguments
  db_group = parser.add_argument_group('database',
                                       'Database connectivity arguments.')
  db_group.add_argument(
      '--db_type',
      choices=['mysql+mysqlconnector', 'sqlite'],
      default='sqlite',
      help='Which database type should be used.')
  db_group.add_argument(
      '--db_user', default='uwsolar', help='The database user.')
  db_group.add_argument(
      '--db_password', default='', help='The database password.')
  db_group.add_argument(
      '--db_host', default=':memory:', help='The database host.')
  db_group.add_argument(
      '--db_name', default='uwsolar', help='The database name.')

  return parser.parse_args()


def config_options_from_json(obj,
                             topic_id_override=None,
                             topic_name_override=None,
                             sample_rate_override=None,
                             spread_override=None):
  """Creates data generation configuration entries from a JSON object.

  Args:
    obj: The JSON object to be converted.
    topic_id_override: An override for the topic ID value.
    topic_name_override: An override for the topic name value.
    sample_rate_override: An override for the sample rate value.
    spread_override: An override for the spread value.

  Returns:
    A list of DataOptions objects.

  Raises:
    ValueError: When a required parameter is not present.
  """
  options = []
  for item in obj:
    if 'start' not in item or 'end' not in item:
      raise ValueError('A start and end date are required.')

    if not ('topic_id' in item or topic_id_override):
      raise ValueError('A topic ID is required.')

    if not ('topic_name' in item or topic_name_override):
      raise ValueError('A topic name is required.')

    start = dateutil.parser.parse(item.get('start'))
    end = dateutil.parser.parse(item.get('end'))
    topic_id = item.get('topic_id', topic_id_override)
    topic_name = item.get('topic_name', topic_name_override)
    period = float(item.get('period', DEFAULT_PERIOD))
    amplitude_cos = float(item.get('amplitude_cos', DEFAULT_AMPLITUDE_COS))
    amplitude_sin = float(item.get('amplitude_sin', DEFAULT_AMPLITUDE_SIN))
    amplitude_offset = float(
        item.get('amplitude_offset', DEFAULT_AMPLITUDE_OFFSET))
    spread = float(item.get('spread', DEFAULT_SPREAD))

    if topic_id_override:
      topic_id = topic_id_override

    if topic_name_override:
      topic_name = topic_name_override

    if sample_rate_override:
      sample_rate = sample_rate_override
    else:
      sample_rate = item.get('sample_rate', DEFAULT_SAMPLE_RATE)

    if spread_override:
      spread = spread_override
    else:
      spread = item.get('spread', DEFAULT_SPREAD)

    options.append(
        DataOptions(start, end, topic_id, topic_name, sample_rate, period,
                    amplitude_cos, amplitude_sin, amplitude_offset, spread))

  return options


def create_topic(topics, options):
  """Creates a topic for the given data generation options.

  Args:
    topics: A dictionary of existing topics, keyed by the topic ID.
  """
  if options.topic_id in topics:
    return

  topic = model.Topic(options.topic_id, options.topic_name)
  topics[options.topic_id] = topic


def generate_datum(options, ts):
  """Generates a datum object for the given timestamp and topic.

  Args:
    options: The configuration options for the current data generation run.
    ts: The datum timestamp.

  Returns:
    A populated datum object, ready for insertion.
  """
  # value = offset + A_cos * cos(omega * t) + A_sin * sin(omega * t) + fuzz factor
  omega = 2 * math.pi / options.period
  seconds = (ts - options.start).total_seconds()
  fuzz = random.uniform(-options.spread, options.spread)
  x = omega * seconds
  value = (options.amplitude_offset + options.amplitude_cos * math.cos(x) +
           options.amplitude_sin * math.sin(x) + fuzz)

  datum = model.Datum(ts, options.topic_id, str(value))
  return datum


def create_data(data, options):
  """Creates data for a given configuration options.

  Args:
    data: Previously generated data.
    options: The configuration options for the current data generation run.
  """
  cur = options.start
  delta = datetime.timedelta(seconds=(1 / options.sample_rate))

  samples = math.floor(
      (options.end - options.start).total_seconds() * options.sample_rate)
  for _ in range(0, samples):
    datum = generate_datum(options, cur)
    if cur in data:
      datum.value_string = str(
          float(datum.value_string) + float(data[cur].value_string))

    data[cur] = datum
    cur += delta


def write_to_db(args, options, topics, data):
  """"Writes topics and data to the database.

  Args:
    args: Arguments containing DB connectivity options.
    topics: A list of topics to be written.
    data: A list of data to be written.
  """
  if args.db_type == 'sqlite':
    dsn = '%s:///%s' % (args.db_type, args.db_host)
  else:
    dsn = '%s://%s:%s@%s/%s' % (args.db_type, args.db_user, args.db_password,
                                args.db_host, args.db_name)
  engine = sqlalchemy.create_engine(dsn)
  session = sqlalchemy.orm.Session(engine)

  # Write topics.
  for topic in topics.values():
    session.merge(topic)

  # Delete any existing data values.
  for i in options:
    q = session.query(model.Datum).filter(model.Datum.ts >= i.start).filter(
        model.Datum.ts <= i.end)
    logging.info('Replacing %d existing records.', q.count())
    q.delete(synchronize_session=False)

  # Write data.
  session.add_all(data.values())
  session.commit()
  session.close()


def main():
  """Parses the command line, generates data, and adds it into the database."""
  args = parse_arguments()
  logging.basicConfig(level=logging.getLevelName(args.log_level))

  # Read data generation options.
  with open(args.input_file, 'r') as f:
    # jsmin strips comments from the JSON file.
    config = json.loads(jsmin.jsmin(f.read()))
    options = config_options_from_json(config, args.topic_id, args.topic_name,
                                       args.sample_rate, args.spread)
  # Generate data.
  data = {}
  topics = {}
  for i in options:
    logging.info('Generating data with the following options: %s', i)
    create_topic(topics, i)
    create_data(data, i)

  logging.info('Topics generated: %d, data generated: %d', len(topics),
               len(data))

  # Write data to database.
  if topics or data:
    write_to_db(args, options, topics, data)


if __name__ == '__main__':
  main()
