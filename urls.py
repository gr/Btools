# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^query/$', views.query, {'tpl':'debug-query.html'}),
    (r'^(?P<debug>(debug)+)/(?P<db_url>[\w\s]+)/(?P<id>[\w\d\\\\]+)/*$', views.get_book, {'tpl':'debug.html'}),
    (r'^tpl/(?P<tpl>[\w\s]+)', views.render_template)
)
