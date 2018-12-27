from django.urls import path
from . import views

urlpatterns = [
    path('ping', views.get_ping),
    path('metric/<str:name>', views.get_metric),
    path('collect/<int:iterations>/<int:wait_time>', views.collect)
]
