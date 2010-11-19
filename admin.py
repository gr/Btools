# -*- coding: utf-8 -*-
from django.contrib import admin
from models import BookDB, BookSet


class BookDBAdmin(admin.ModelAdmin):
    search_fields = ['name', 'host', 'port', 'db', 'encoding', 'about']
    list_filter = ['name', 'host', 'port', 'db', 'encoding', 'about']
    ordering = ['name', 'host', 'port', 'db', 'encoding', 'about']
    list_display = ('name', 'host', 'port', 'db', 'encoding')
    
class BookSetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'query_type', 'query', 'about']
    list_filter = ['db', 'query_type', 'view_me']
    ordering = ['name', 'time']
    list_display = ('name', 'view_me', 'db', 'query_type', 'query', 'time', 'last_time_update', 'number_of_books')


admin.site.register(BookSet, BookSetAdmin)    
admin.site.register(BookDB, BookDBAdmin)
