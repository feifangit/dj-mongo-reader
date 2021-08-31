from django.conf.urls import url
from . import views

urlpatterns = [
                       url(r"^$", views.blank, name="dj-mongo-reader-root"),
                       url(r"^info/$", views.info),
                       url(r"^(?P<db>\w+)/(?P<col>\w+)/$", views.blank, name="dj-mongo-reader-col"),
                       url(r"^(?P<db>\w+)/(?P<col>\w+)/_(?P<cmd>\w+)$", views.restcall, name="dj-mongo-reader-cmd"),
                       url(r"^(?P<db>\w+)/(?P<col>\w+)/exportcsv/$", views.exportcsv, {"cmd":"exportcsv"}, name="dj-mongo-reader-exportcsv"),
]
