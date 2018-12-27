"""uwsolar URL Configuration

The "urlpatterns" list routes URLs to views. For more information please see
https://docs.djangoproject.com/en/2.1/topics/http/urls/.

    - Function views: path('', views.home, name='home')
    - Class-based views: path('', Home.as_view(), name='home')
    - Including another URLconf: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('collector/', include('collector.urls')),
    path('admin/', admin.site.urls)
]
