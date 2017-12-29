"""Encoders and decoders for model objects."""

import model

def encode_topic(obj):
  """Encodes a Topic object for msgpack serialization.

  Args:
    obj: The object being serialized.

  Returns:
    A list containing Topic properties.

  Raises:
    TypeError: When the object is not a Topic.
  """
  if isinstance(obj, model.Topic):
    return [obj.topic_id, obj.topic_name]
  raise TypeError('Unknown type: %r' % obj)

def encode_datum(obj):
  """Encodes a Datum object for msgpack serialization.

  Args:
    obj: The object being serialized.

  Returns:
    A list containing Datum properties.

  Raises:
    TypeError: When the object is not a Datum.
  """
  if isinstance(obj, model.Datum):
    return [obj.ts.isoformat(), obj.topic_id, obj.value_string]
  raise TypeError('Unknown type: %r' % obj)
