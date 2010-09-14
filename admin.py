# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class BookDBAdmin(admin.ModelAdmin):
    search_fields = ['name', 'host', 'port', 'db', 'encoding', 'about']
    list_filter = ['name', 'host', 'port', 'db', 'encoding', 'about']
    ordering = ['name', 'host', 'port', 'db', 'encoding', 'about']
    list_display = ('name', 'host', 'port', 'db', 'encoding')


admin.site.register(BookDB, BookDBAdmin)
