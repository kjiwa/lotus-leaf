"""A module containing object used throughout the UW Solar application."""

import collections

# A metadata object. This object describes known metadata for a particular
# Topic.
Metadata = collections.namedtuple('Meta', ['topic_id', 'metadata'])

# A topic object. A topic is a tuple containing the name of a meter (e.g.
# "UW/Maple/eaten_meter") and an associated metric (e.g. Angle_I_A, freq, pf,
# etc.).
Topic = collections.namedtuple('Topic', ['topic_id', 'topic_name'])

# A data object. This object represents a value for a topic at a particular
# time.
Datum = collections.namedtuple('Datum', ['ts', 'topic_id', 'value_string'])
