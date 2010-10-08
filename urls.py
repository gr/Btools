# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns(
    (r'^test/*$', 'apps.Btools.views.test', {'tpl':'test.html'}),
)
