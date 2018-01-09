"""Encoders and decoders for model objects."""

import json
import model


class TopicEncoder(json.JSONEncoder):
  """A Topic to JSON encoder."""

  # pylint: disable=arguments-differ,method-hidden
  def default(self, obj):
    """Encodes a Topic object for JSON serialization.

    Args:
      obj: The object being serialized.

    Returns:
      A list containing Topic properties.

    Raises:
      TypeError: When the object is not a Topic.
    """
    if isinstance(obj, model.Topic):
      return [obj.topic_id, obj.topic_name]
    return super().default(obj)


class DatumEncoder(json.JSONEncoder):
  """A Topic to JSON encoder."""

  # pylint: disable=arguments-differ,method-hidden
  def default(self, obj):
    """Encodes a Datum object for JSON serialization.

    Args:
      obj: The object being serialized.

    Returns:
      A list containing Datum properties.

    Raises:
      TypeError: When the object is not a Datum.
    """
    if isinstance(obj, model.Datum):
      return [obj.ts.isoformat(), obj.topic_id, obj.value_string]
    return super().default(obj)
