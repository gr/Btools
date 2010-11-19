# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views
from models import BookDB

dbs=BookDB.objects.all()
if dbs.__len__ > 1:
    regexp = '|'.join([db.url for db in dbs])
elif dbs.__len__ == 1:
    regexp = dbs[0].url

urlpatterns = patterns('',
    (r'^query/$', views.query, {'tpl':'debug-query.html'}),  
)

if regexp:
    urlpatterns += patterns('',
    (r'^(?P<debug>(debug/)+)(?P<db_url>('+regexp+'))/(?P<id>[\w\d\\\\]+)/*$', views.get_book, {'tpl':'debug.html'}),
    (r'^tpl/(?P<tpl>[\w\s]+)', views.render_template)
)
