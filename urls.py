# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'debug_index.html'}),
    (r'^tpl/(?P<template>[\w\s\.\-]+)', 'django.views.generic.simple.direct_to_template'),
    (r'^query/$', views.query, {'tpl':'debug-query.html'}),
    (r'^(?P<db_url>[\w\s]+)/(?P<id>[\w\d\\\\]+)/*$', views.get_book, {'debug':'debug','tpl':'debug.html'}),
)
