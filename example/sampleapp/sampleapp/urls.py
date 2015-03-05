from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sampleapp.views.readme', name='home'),
    url(r'^query/$', 'sampleapp.views.query',),
    url(r'^mongo/', include('djmongoreader.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
