"""A program that creates the default set of UW Solar topics."""

import argparse
import sqlalchemy
from db import db_model

ALDER_TOPICS = [db_model.Topic(8, 'UW/Alder/eaton_meter/Angle_I_A'),
                db_model.Topic(11, 'UW/Alder/eaton_meter/Angle_I_B'),
                db_model.Topic(5, 'UW/Alder/eaton_meter/Angle_I_C'),
                db_model.Topic(20, 'UW/Alder/eaton_meter/Angle_V_AN'),
                db_model.Topic(21, 'UW/Alder/eaton_meter/Angle_V_BN'),
                db_model.Topic(19, 'UW/Alder/eaton_meter/Angle_V_CN'),
                db_model.Topic(15, 'UW/Alder/eaton_meter/Current_N'),
                db_model.Topic(17, 'UW/Alder/eaton_meter/freq'),
                db_model.Topic(12, 'UW/Alder/eaton_meter/pf'),
                db_model.Topic(10, 'UW/Alder/eaton_meter/pf_A'),
                db_model.Topic(9, 'UW/Alder/eaton_meter/pf_B'),
                db_model.Topic(13, 'UW/Alder/eaton_meter/pf_C'),
                db_model.Topic(1, 'UW/Alder/eaton_meter/VA'),
                db_model.Topic(16, 'UW/Alder/eaton_meter/VAR'),
                db_model.Topic(3, 'UW/Alder/eaton_meter/Voltage_AN'),
                db_model.Topic(7, 'UW/Alder/eaton_meter/Voltage_BN'),
                db_model.Topic(4, 'UW/Alder/eaton_meter/Voltage_CN'),
                db_model.Topic(14, 'UW/Alder/eaton_meter/W'),
                db_model.Topic(2, 'UW/Alder/eaton_meter/W_A'),
                db_model.Topic(18, 'UW/Alder/eaton_meter/W_B'),
                db_model.Topic(6, 'UW/Alder/eaton_meter/W_C')]

ELM_TOPICS = [db_model.Topic(29, 'UW/Elm/eaton_meter/Angle_I_A'),
              db_model.Topic(32, 'UW/Elm/eaton_meter/Angle_I_B'),
              db_model.Topic(26, 'UW/Elm/eaton_meter/Angle_I_C'),
              db_model.Topic(41, 'UW/Elm/eaton_meter/Angle_V_AN'),
              db_model.Topic(42, 'UW/Elm/eaton_meter/Angle_V_BN'),
              db_model.Topic(40, 'UW/Elm/eaton_meter/Angle_V_CN'),
              db_model.Topic(36, 'UW/Elm/eaton_meter/Current_N'),
              db_model.Topic(38, 'UW/Elm/eaton_meter/freq'),
              db_model.Topic(33, 'UW/Elm/eaton_meter/pf'),
              db_model.Topic(31, 'UW/Elm/eaton_meter/pf_A'),
              db_model.Topic(30, 'UW/Elm/eaton_meter/pf_B'),
              db_model.Topic(34, 'UW/Elm/eaton_meter/pf_C'),
              db_model.Topic(22, 'UW/Elm/eaton_meter/VA'),
              db_model.Topic(37, 'UW/Elm/eaton_meter/VAR'),
              db_model.Topic(24, 'UW/Elm/eaton_meter/Voltage_AN'),
              db_model.Topic(28, 'UW/Elm/eaton_meter/Voltage_BN'),
              db_model.Topic(25, 'UW/Elm/eaton_meter/Voltage_CN'),
              db_model.Topic(35, 'UW/Elm/eaton_meter/W'),
              db_model.Topic(23, 'UW/Elm/eaton_meter/W_A'),
              db_model.Topic(39, 'UW/Elm/eaton_meter/W_B'),
              db_model.Topic(27, 'UW/Elm/eaton_meter/W_C')]

MAPLE_TOPICS = [db_model.Topic(50, 'UW/Maple/eaton_meter/Angle_I_A'),
                db_model.Topic(53, 'UW/Maple/eaton_meter/Angle_I_B'),
                db_model.Topic(47, 'UW/Maple/eaton_meter/Angle_I_C'),
                db_model.Topic(62, 'UW/Maple/eaton_meter/Angle_V_AN'),
                db_model.Topic(63, 'UW/Maple/eaton_meter/Angle_V_BN'),
                db_model.Topic(61, 'UW/Maple/eaton_meter/Angle_V_CN'),
                db_model.Topic(57, 'UW/Maple/eaton_meter/Current_N'),
                db_model.Topic(59, 'UW/Maple/eaton_meter/freq'),
                db_model.Topic(54, 'UW/Maple/eaton_meter/pf'),
                db_model.Topic(52, 'UW/Maple/eaton_meter/pf_A'),
                db_model.Topic(51, 'UW/Maple/eaton_meter/pf_B'),
                db_model.Topic(55, 'UW/Maple/eaton_meter/pf_C'),
                db_model.Topic(43, 'UW/Maple/eaton_meter/VA'),
                db_model.Topic(58, 'UW/Maple/eaton_meter/VAR'),
                db_model.Topic(45, 'UW/Maple/eaton_meter/Voltage_AN'),
                db_model.Topic(49, 'UW/Maple/eaton_meter/Voltage_BN'),
                db_model.Topic(46, 'UW/Maple/eaton_meter/Voltage_CN'),
                db_model.Topic(56, 'UW/Maple/eaton_meter/W'),
                db_model.Topic(44, 'UW/Maple/eaton_meter/W_A'),
                db_model.Topic(60, 'UW/Maple/eaton_meter/W_B'),
                db_model.Topic(48, 'UW/Maple/eaton_meter/W_C')]

MERCER_TOPICS = [db_model.Topic(71, 'UW/Mercer/nexus_meter/Angle_I_A'),
                 db_model.Topic(74, 'UW/Mercer/nexus_meter/Angle_I_B'),
                 db_model.Topic(68, 'UW/Mercer/nexus_meter/Angle_I_C'),
                 db_model.Topic(83, 'UW/Mercer/nexus_meter/Angle_V_AN'),
                 db_model.Topic(84, 'UW/Mercer/nexus_meter/Angle_V_BN'),
                 db_model.Topic(82, 'UW/Mercer/nexus_meter/Angle_V_CN'),
                 db_model.Topic(78, 'UW/Mercer/nexus_meter/Current_N'),
                 db_model.Topic(80, 'UW/Mercer/nexus_meter/freq'),
                 db_model.Topic(75, 'UW/Mercer/nexus_meter/pf'),
                 db_model.Topic(73, 'UW/Mercer/nexus_meter/pf_A'),
                 db_model.Topic(72, 'UW/Mercer/nexus_meter/pf_B'),
                 db_model.Topic(76, 'UW/Mercer/nexus_meter/pf_C'),
                 db_model.Topic(64, 'UW/Mercer/nexus_meter/VA'),
                 db_model.Topic(79, 'UW/Mercer/nexus_meter/VAR'),
                 db_model.Topic(66, 'UW/Mercer/nexus_meter/Voltage_AN'),
                 db_model.Topic(70, 'UW/Mercer/nexus_meter/Voltage_BN'),
                 db_model.Topic(67, 'UW/Mercer/nexus_meter/Voltage_CN'),
                 db_model.Topic(77, 'UW/Mercer/nexus_meter/W'),
                 db_model.Topic(65, 'UW/Mercer/nexus_meter/W_A'),
                 db_model.Topic(81, 'UW/Mercer/nexus_meter/W_B'),
                 db_model.Topic(69, 'UW/Mercer/nexus_meter/W_C')]


def parse_arguments():
  """Parses command line arguments.

  Returns:
    An object containing parsed arguments.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('--log_level', default='INFO',
                      help='The logging threshold.')

  # Database connectivity arguments
  parser.add_argument('--db_type', choices=['mysql+mysqlconnector', 'sqlite'],
                      default='sqlite',
                      help='Which database type should be used.')
  parser.add_argument('--db_user', default='uwsolar', help='The database user.')
  parser.add_argument('--db_password', default='',
                      help='The database password.')
  parser.add_argument('--db_host', default=':memory:',
                      help='The database host.')
  parser.add_argument('--db_name', default='uwsolar', help='The database name.')

  return parser.parse_args()


def write_to_db(args, topics):
  """"Writes topics to the database.

  Args:
    args: Arguments containing DB connectivity options.
    topics: A list of topics to be written.
  """
  if args.db_type == 'sqlite':
    dsn = '%s:///%s' % (args.db_type, args.db_host)
  else:
    dsn = '%s://%s:%s@%s/%s' % (
      args.db_type, args.db_user, args.db_password, args.db_host, args.db_name)
  engine = sqlalchemy.create_engine(dsn)
  session = sqlalchemy.orm.Session(engine)

  # Write topics.
  for topic in topics:
    session.merge(topic)

  session.commit()
  session.close()


def main():
  """Parses command line arguments and writes topics to the database."""
  write_to_db(parse_arguments(),
              ALDER_TOPICS + ELM_TOPICS + MAPLE_TOPICS + MERCER_TOPICS)


if __name__ == '__main__':
  main()
