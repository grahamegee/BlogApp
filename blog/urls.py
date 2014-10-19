from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.blog),
    url(r'^dashboard/$', views.dashboard),
    url(r'^dashboard/new/$', views.newentry),
    url(r'^dashboard/(?P<pk>[0-9]+)/edit/$', views.editentry),
)
