import time
from . import models, panel_api
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_safe


@require_safe
def get_ping(request):
    return http.HttpResponse()


@require_GET
def get_metric(request, name):
    return http.HttpResponse(content=panel_api.client().get_metric(name))


@csrf_exempt
@require_POST
def collect(request, iterations, wait_time):
    client = panel_api.client()
    topic_ids_by_name = {t.topic_name: t for t in models.Topic.objects.all()}
    for _ in range(0, iterations):
        data = [models.TopicDatum(topic=topic_ids_by_name[m.topic_name], value_string=str(client.get_metric(m.name)))
                for m in client.metrics.values()]
        for d in data:
            d.save()

        time.sleep(wait_time)

    return http.HttpResponse()
