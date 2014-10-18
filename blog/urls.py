from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.blog),
    url(r'^dashboard/', views.dashboard),
)
