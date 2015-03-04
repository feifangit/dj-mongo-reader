from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r"^$", "info"),
                       url(r"(?P<db>\w+)/(?P<col>\w+)/(?P<cmd>\w+)$", views.restcall, name="mongo-restcall"),
                       )
