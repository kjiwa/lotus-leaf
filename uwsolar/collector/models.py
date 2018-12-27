from django.db import models
from django.utils.timezone import now


class Topic(models.Model):
    db_table = 'topics'
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=512)


class Metadata(models.Model):
    db_table = 'meta'
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    metadata = models.TextField()


class TopicDatum(models.Model):
    db_table = 'data'
    ts = models.DateTimeField(default=now)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, db_column='topic_id')
    value_string = models.TextField()
