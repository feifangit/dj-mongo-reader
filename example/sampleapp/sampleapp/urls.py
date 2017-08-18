from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

admin.autodiscover()


urlpatterns = [
    url(r'^$', views.readme, name='home'),
    url(r'^query/$', views.query,),
    url(r'^mongo/', include('djmongoreader.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)